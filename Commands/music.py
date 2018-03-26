import asyncio
import functools
import discord
from discord.ext import commands
import youtube_dl
import os

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
    
    def __init__(self, songInfo, fileName):
        self.songInfo = songInfo
        self.fileName = fileName
        super().__init__(discord.FFmpegPCMAudio(fileName, before_options="-nostdin", options="-vn"))


class MusicPlayer:

    def __init__(self, bot, ctx):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.DLqueue = asyncio.Queue()
        self.notDL = asyncio.Event()
        self.notDL.set()
        self.playing = asyncio.Event()
        self.guild = ctx.guild
        self.channel = ctx.channel
        self.lastSong = None
        self.task = self.bot.loop.create_task(self.download())

    async def download(self):
        while True:
            if self.DLqueue.empty():
                pass
            else:
                self.notDL.clear()
                songToDL = await self.DLqueue.get()
                func = functools.partial(ytdl.extract_info, songToDL["query"])
                data = await self.bot.loop.run_in_executor(None, func)
                if "entries" in data:
                    data = data["entries"][0]
                func2 = functools.partial(ytdl.prepare_filename, data)
                filename = await self.bot.loop.run_in_executor(None, func2)
                SongObject = Song(songToDL, filename)
                await self.queue.put(SongObject)
                tempchannel = songToDL["channel"]
                await tempchannel.send(f"Added `{data['title']}` to the queue. (Requested by `{songToDL['requester'].name}`).")
                self.notDL.set()
            await asyncio.sleep(1)


    async def PlayerRecurse(self):
        while not self.queue.empty():
            self.playing.clear()
            songToPlay = await self.queue.get()
            await asyncio.sleep(1.5)
            self.lastSong = songToPlay.fileName
            self.guild.voice_client.play(songToPlay, after=lambda error: self.bot.loop.call_soon_threadsafe(self.playing.set))
            await self.playing.wait()
            func = functools.partial(os.remove, self.lastSong)
            await self.bot.loop.run_in_executor(None, func)
        await self.guild.voice_client.disconnect()

class Music:

    def __init__(self, bot):
        self.bot = bot
        self.guildPlayers = {}

    def get_player(self, ctx):
        try:
            player = self.guildPlayers[str(ctx.guild.id)]
        except KeyError:
            player = MusicPlayer(self.bot, ctx)
            self.guildPlayers[str(ctx.guild.id)] = player
        return player

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

    @commands.command(name="pause")
    @commands.guild_only()
    async def _pause(self, ctx):
        """Pauses the player, if playing a song."""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            return await ctx.send("Not playing any songs.")
        ctx.guild.voice_client.pause()

    @commands.command(name="resume")
    @commands.guild_only()
    async def _resume(self, ctx):
        """Resumes the player, if paused."""
        if ctx.voice_client is None or not ctx.voice_client.is_paused():
            return await ctx.send("Not connected to a voice channel or not paused.")
        ctx.guild.voice_client.resume()

    @commands.command(name="leave")
    @commands.guild_only()
    async def leave(self, ctx):
        """Leaves a voice channel, if connected."""
        if ctx.guild.voice_client is None:
            await ctx.send("Not connected to any voice channel.")
            return
        await ctx.guild.voice_client.disconnect()
        del self.guildPlayers[str(ctx.guild.id)]

    @commands.command(name="volume")
    @commands.guild_only()
    async def volume(self, ctx, vol: int):
        """Change the volume of the song, if playing."""
        if not 0 < vol < 100:
            return await ctx.send("Please specify a value between 0 - 100 only.")
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            return await ctx.send("Not playing any songs.")
        ctx.voice_client.source.volume = float(vol / 100)
        await ctx.send(f"Set the player volume to {vol}")

    @commands.command(name="skip")
    @commands.guild_only()
    async def _skip(self, ctx):
        """Skip the current song."""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            return await ctx.send("Not playing any songs.")
        ctx.voice_client.stop()

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
        player = self.get_player(ctx)
        if not player.notDL.is_set():
            await player.notDL.wait()
        await player.PlayerRecurse()
    
    @commands.command(name="add")
    @commands.guild_only()
    async def _add(self, ctx, *, args=None):
        """Adds a song to the queue."""
        player = self.get_player(ctx)
        if args is None:
            return await ctx.send("Please make a query!")
        infoDict = {
            "requester": ctx.author,
            "channel": ctx.message.channel,
            "query": args
        }
        await player.DLqueue.put(infoDict)

def setup(bot):
    bot.add_cog(Music(bot))