import functools
import re
import asyncio
from io import BytesIO
from discord.ext import commands
import discord
from Utils import ImageClient
import random



class Images:
    
    def __init__(self, bot):
        self.bot = bot
        self.imageClient = ImageClient.ImageClient(bot)

    @commands.command(name="illegal")
    async def illegal(self, ctx, *, args=None):
        """Ask US President Donald Trump to make something illegal."""
        if args is None:
            await ctx.send("Please provide something to make it illegal.")
            return
        if len(args) > 10 or len(args) < 1:
            await ctx.send("You can make only 1 to 10 lettered things illegal.")
            return
        elif not bool(re.match('^[a-zA-Z0-9]+$', args)):
            await ctx.send("Oops! Only alphanumeric characters are allowed.")
            return
        
        payload = {"task": "gif", "word": args.upper()}

        async with ctx.message.channel.typing():
            message = await ctx.send(f"Convincing US President Donald Trump to make `{args}` illegal.")
            async with self.bot.session.post("https://is-now-illegal.firebaseio.com/queue/tasks.json", json=payload) as resp:
                pass
            await asyncio.sleep(5)
            url = f"https://storage.googleapis.com/is-now-illegal.appspot.com/gifs/{args.upper()}.gif"
            async with self.bot.session.get(url) as resp:
                image = await resp.read()
            await ctx.send(file=discord.File(BytesIO(image), "illegal.gif"))
            await message.delete()
        
    @commands.command(name="beautiful")
    async def beautiful(self, ctx, user: discord.Member = None):
        """This... this is beautiful!"""
        member = user or ctx.author
        async with ctx.typing():
            avatar = await self.imageClient.getAvatar(user=member, size=128)
            func = functools.partial(self.imageClient.beautify, avatar)
            image = await self.bot.loop.run_in_executor(None, func)
            await ctx.send(file=discord.File(fp=image, filename="beautiful.png"))

    @commands.command(name="delet")
    async def delet(self, ctx, user: discord.Member = None):
        """Delet this garbage!"""
        member = user or ctx.author
        async with ctx.typing():
            avatar = await self.imageClient.getAvatar(user=member, size=128)
            func = functools.partial(self.imageClient.deletify, avatar, f"{member.name}#{member.discriminator}")
            image = await self.bot.loop.run_in_executor(None, func)
            await ctx.send(file=discord.File(fp=image, filename="delet.png"))

    @commands.command(name="robot")
    async def robot(self, ctx, *, args=None):
        """See a unique robot image from any text."""
        if args is None:
            args = ctx.author.name
        randomInt = random.randrange(1, 3)
        async with ctx.typing():
            image = await self.imageClient.getRobotImage(args, randomInt)
            file = discord.File(fp=image, filename=f"{args}.png")
            await ctx.send(file=file)

    @commands.command(name="thuglife")
    async def thuglife(self, ctx, user: discord.Member = None):
        """Thug Life....."""
        member = user or ctx.author
        async with ctx.typing():
            avatar = await self.imageClient.getAvatar(user=member, size=512)
            func = functools.partial(self.imageClient.thugLife, avatar)
            image = await self.bot.loop.run_in_executor(None, func)
            await ctx.send(file=discord.File(fp=image, filename="thuglife.png"))


def setup(bot):
    bot.add_cog(Images(bot))