import discord
from discord.ext import commands
from Utils import comicstrip

class Comics:
    """
    Read the popular comic strips published today, or fetch comics by random date.
    """


    def __init__(self, bot):
        self.bot = bot
        self.comicClient = comicstrip.Client(bot)

    @commands.command()
    async def dilbert(self, ctx, mode: str = None):
        """
        Get a random Dilbert Comic Strip or read todays. See help for more.
        Use 'today' flag to get todays comic. 
        """
        if mode == "today":
            url = await self.comicClient.getDilbert(mode=1)
        else:
            url = await self.comicClient.getDilbert(mode=0)
        embed = discord.Embed(color=0x42B6F4)
        embed.set_image(url=url)
        embed.set_author(name="Dilbert 📰", url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def garfield(self, ctx, mode: str = None):
        """
        Get a random Garfield Comic Strip or read todays. See help for more.
        Use 'today' flag to get todays comic. 
        """
        if mode == "today":
            url = await self.comicClient.getGarfield(mode=1)
        else:
            url = await self.comicClient.getGarfield(mode=0)
        embed = discord.Embed(color=0x42B6F4)
        embed.set_image(url=url)
        embed.set_author(name="Garfield 📰", url=url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Comics(bot))