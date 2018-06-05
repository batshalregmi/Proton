from discord.ext import commands
import discord
import urllib.parse


class Utilities:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="isgd")
    async def isgd(self, ctx, *, url):
        """Shortens the url provided by you."""
        async with self.bot.session.get(f"https://is.gd/create.php?format=simple&url={urllib.parse.quote(url)}") as resp:
            text = await resp.text()
        if "error" in text.lower():
            embed = discord.Embed(description=f"**{text}**")
            return await ctx.send(embed=embed)
        embed = discord.Embed(description=f"Your shortened URL is **<{text}>**")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))