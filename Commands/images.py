import re
import asyncio
from io import BytesIO
from discord.ext import commands
import discord

class Images:
    
    def __init__(self, bot):
        self.bot = bot
    
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
            await ctx.send("Oops! Non-standard Unicode characters are now illegal.")
            return
        
        payload = {"task": "gif", "word": args.upper()}

        async with ctx.message.channel.typing():
            message = await ctx.send(f"Convincing US President Donald Trump to make `{args}` illegal.")
            async with self.bot.session.post("https://is-now-illegal.firebaseio.com/queue/tasks.json", json=payload) as resp:
                pass
            await asyncio.sleep(5.0)
            async with self.bot.session.get(f"https://is-now-illegal.firebaseio.com/gifs/{args.upper()}.json") as resp:
                pass
            url = f"https://storage.googleapis.com/is-now-illegal.appspot.com/gifs/{args.upper()}.gif"
            async with self.bot.session.get(url) as resp:
                image = await resp.read()
            await ctx.send(file=discord.File(BytesIO(image), "illegal.gif"))
            await message.delete()

def setup(bot):
    bot.add_cog(Images(bot))