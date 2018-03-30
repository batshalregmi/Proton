import os
import asyncio
import functools
from datetime import datetime
import youtube_dl
import discord
from discord.ext import commands

ytdlOpts = {
    "format": "bestaudio/best",
    "outtmpl": "Temp/%(extractor)s-%(id)s-%(title)s-%(autonumber)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": False,
    "default_search": "auto",
    "source_address": "0.0.0.0"
}

ytdl = youtube_dl.YoutubeDL(ytdlOpts)


class Song(discord.PCMVolumeTransformer):
    
    def __init__(self, songInfo, fileName, data):
        self.songInfo = songInfo
        self.fileName = fileName
        self.title = data.get('title')
        self.description = data.get('description')
        self.thumb = data.get('thumbnail')
        self.uploader = data.get('uploader')
        self.duration = data.get('duration')
        self.uploadDate = data.get('upload_date')
        self.uploadDate = self.uploadDate[6:8] + "/" + self.uploadDate[4:6] + "/" + self.uploadDate[:4]  
        super().__init__(discord.FFmpegPCMAudio(fileName, before_options="-nostdin", options="-vn"))


class MusicPlayer:

    def __init__(self, bot, ctx):
        self.bot = bot
        self.loop = bot.loop
        self.unsafe_queue = []
        self.queue = asyncio.Queue()
        self.DLqueue = asyncio.Queue()
        self.playing = asyncio.Event()
        self.guild = ctx.guild
        self.lastSong = None
        self.task = self.loop.create_task(self.download())

    async def download(self):
        while True:
            if self.DLqueue.empty():
                pass
            else:
                songToDL = await self.DLqueue.get()
                func = functools.partial(ytdl.extract_info, songToDL["query"])
                data = await self.loop.run_in_executor(None, func)
                if "entries" in data:
                    data = data["entries"][0]
                func2 = functools.partial(ytdl.prepare_filename, data)
                filename = await self.loop.run_in_executor(None, func2)
                SongObject = Song(songToDL, filename, data)
                self.unsafe_queue.append(SongObject)
                await self.queue.put(SongObject)
                tempchannel = songToDL["channel"]
                await tempchannel.send(f"Added `{data['title']}` to the queue. (Requested by `{songToDL['requester'].name}`).")
            await asyncio.sleep(1)

    async def PlayerStart(self, channel):
        while not self.queue.empty():
            self.playing.clear()
            songToPlay = await self.queue.get()
            self.unsafe_queue.pop(0)
            await asyncio.sleep(1.5)
            self.lastSong = songToPlay.fileName
            self.guild.voice_client.play(songToPlay, after=lambda error: self.loop.call_soon_threadsafe(self.playing.set))
            await channel.send(f"Now Playing : `{songToPlay.title}` as requested by `{songToPlay.songInfo['requester']}`.")
            await self.playing.wait()
            songToPlay.cleanup()
            func = functools.partial(os.remove, self.lastSong)
            await self.loop.run_in_executor(None, func)
        await channel.send("We have run out of tunes, queue up some more!")
        await self.guild.voice_client.disconnect()

class Music:

    def __init__(self, bot):
        self.bot = bot
        self.guildPlayers = {}

    def parseUploadTime(self, secs):
        mins, secsLeftOver = divmod(secs, 60)
        if mins > 60:
            hours = mins / 60
            mins = mins % 60
        else:
            hours = 0
        return f"{hours} hours, {mins} minutes and {secsLeftOver} seconds."


    def get_player(self, ctx):
        try:
            player = self.guildPlayers[str(ctx.guild.id)]
        except KeyError:
            player = MusicPlayer(self.bot, ctx)
            self.guildPlayers[str(ctx.guild.id)] = player
        return player

    async def close_all_clients(self):
        try:
            for i in self.guildPlayers.keys():
                await self.guildPlayers[i].guild.voice_client.disconnect()
        except Exception:
            pass

    @commands.command(name="join")
    @commands.guild_only()
    async def join(self, ctx):
        """Joins the channel the user is connected to."""
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send("User not connected to any channel.")
            return
        await channel.connect()
        await ctx.send(f"Successfully joined channel `{ctx.voice_client.channel.name}` as requested by `{ctx.author.name}.`")

    @commands.command(name="pause")
    @commands.guild_only()
    async def _pause(self, ctx):
        """Pauses the player, if playing a song."""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            return await ctx.send("Not playing any songs.")
        ctx.guild.voice_client.pause()
        await ctx.send("Paused the song.")

    @commands.command(name="resume")
    @commands.guild_only()
    async def _resume(self, ctx):
        """Resumes the player, if paused."""
        if ctx.voice_client is None or not ctx.voice_client.is_paused():
            return await ctx.send("Not connected to a voice channel or not paused.")
        ctx.guild.voice_client.resume()
        await ctx.send("Resumed the song.")

    @commands.command(name="leave", aliases=["stop"])
    @commands.guild_only()
    async def leave(self, ctx):
        """Leaves a voice channel, if connected."""
        if ctx.guild.voice_client is None:
            await ctx.send("Not connected to any voice channel.")
            return
        await ctx.guild.voice_client.disconnect()
        try:
            player = self.get_player(ctx)
            player.task.cancel()
            del self.guildPlayers[str(ctx.guild.id)]
        except KeyError:
            pass
        await ctx.send("Successfully left the voice channel.")

    @commands.command(name="volume")
    @commands.guild_only()
    async def volume(self, ctx, vol: int):
        """Change the volume of the song, if playing."""
        if not 0 < vol <= 100:
            return await ctx.send("Please specify a value between 0 - 100 only.")
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            return await ctx.send("Not playing any songs.")
        ctx.voice_client.source.volume = float(vol / 100)
        await ctx.send(f"Set the player volume to {vol}.")

    @commands.command(name="skip")
    @commands.guild_only()
    async def _skip(self, ctx):
        """Skip the current song."""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            return await ctx.send("Not playing any songs.")
        ctx.voice_client.stop()
        await ctx.send("Skipped the current song.")

    @commands.command(name="play")
    @commands.guild_only()
    async def play(self, ctx):
        """Starts playing songs in the playlist."""
        if ctx.guild.voice_client is None:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                return await ctx.send("User not connected to any channel.")
            await channel.connect()
        if ctx.voice_client.is_playing():
            return await ctx.send("Currently songs are being played.")
        player = self.get_player(ctx)
        await player.PlayerStart(channel=ctx.message.channel)
    
    @commands.command(name="add")
    @commands.guild_only()
    async def _add(self, ctx, *, args=None):
        """Adds a song to the queue."""
        player = self.get_player(ctx)
        if args is None:
            return await ctx.send("Please make a query!")
        DLRequest = {
            "requester": ctx.author,
            "channel": ctx.message.channel,
            "query": args
        }
        await player.DLqueue.put(DLRequest)

    @commands.command(name="queue")
    @commands.guild_only()
    async def queue(self, ctx):
        """Shows the songs currently in the queue."""
        player = self.get_player(ctx)
        if len(player.unsafe_queue) == 0:
            return await ctx.send("Queue is empty. Add some more songs.")
        base = "**Queue : **\n```"
        for i in range(len(player.unsafe_queue)):
            base = base + str(i) + ") " + player.unsafe_queue[i].title + "\n"
        base = base + "```"
        await ctx.send(base)

    @commands.command(name="np")
    @commands.guild_only()
    async def _np(self, ctx):
        """Shows some information about the currently playing song."""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            return await ctx.send("Currently, no song is being played.")
        source = ctx.voice_client.source
        embed = discord.Embed(title=f"Now Playing : {source.title}", description=source.description[:500] + " ...", color=0xF4426B)
        embed.add_field(name="Uploader", value=source.uploader, inline=True)
        embed.add_field(name="Duration", value=self.parseUploadTime(source.duration), inline=True)
        embed.add_field(name="Upload Date", value=source.uploadDate, inline=True)
        embed.set_thumbnail(url=source.thumb)
        embed.set_footer(text=f"{self.bot.user.name} {datetime.now().strftime('%Y-%m-%d')}", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Music(bot))