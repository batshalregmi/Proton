import urllib.parse
from datetime import datetime
import discord
from discord.ext import commands


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

    @commands.command(name="avatar", aliases=["pfp"])
    async def _avatar(self, ctx, *, user: discord.User = None):
        """Displays a users avatar/profile picture."""
        if user is None:
            user = ctx.author
        embed = discord.Embed(title=f"{user.name}'s Avatar")
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="ping", aliases=["latency"])
    async def _ping(self, ctx):
        """Latency and API response times."""
        emoji = "\N{TABLE TENNIS PADDLE AND BALL}"
        sentMessage = await ctx.send("\N{TABLE TENNIS PADDLE AND BALL} Pong! (Calculating Ping).")
        pingInMs = int((sentMessage.created_at - ctx.message.created_at).microseconds/1000)
        await sentMessage.edit(content=f"{emoji} Pong! **WS Latency:** `{int(self.bot.latency*1000)}`ms. **Roundtrip (User <-> Bot):** `{pingInMs}`ms.")

def setup(bot):
    bot.add_cog(Utilities(bot))
