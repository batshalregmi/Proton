from functools import partial
import re
import asyncio
from io import BytesIO
from discord.ext import commands
import discord
from PIL import Image


class Images:
    
    def __init__(self, bot):
        self.bot = bot

    async def get_avatar(self, user):
        avatar_url = user.avatar_url_as(format="png", static_format="png", size=128)
        async with self.bot.session.get(avatar_url) as resp:
            avatar_bytes = await resp.read()
        return avatar_bytes

    def beautify(self, avatar_bytes):
        with Image.open("Assets/Images/plate_beautiful.png") as plate:
            with Image.open(BytesIO(avatar_bytes)) as avatar:
                with Image.new("RGB", (497, 559)) as canvas:
                    canvas.paste(avatar, (335, 35), mask=avatar)
                    canvas.paste(avatar, (337, 315), mask=avatar)
                    canvas.paste(plate, (0, 0), mask=plate)
                    buffer = BytesIO()
                    canvas.save(buffer, "PNG")
        buffer.seek(0)
        return buffer

    @commands.command(name="illegal")
    async def illegal(self, ctx, *, args=None):
        """Ask US Presiden Donald Trump to make something illegal."""
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
            async with self.bot.session.get(f"https://is-now-illegal.firebaseio.com/gifs/{args.upper()}.json") as resp:
                pass
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
            avatar = await self.get_avatar(member)
            func = partial(self.beautify, avatar)
            image = await self.bot.loop.run_in_executor(None, func)
            await ctx.send(file=discord.File(fp=image, filename="beautiful.png"))

def setup(bot):
    bot.add_cog(Images(bot))