import discord
from discord.ext import commands


class Animals:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dog", aliases=["puppy", "doge"])
    async def dog(self, ctx):
        """Get a random dog image."""
        url = "https://dog.ceo/api/breeds/image/random"
        async with self.bot.session.get(url) as resp:
            json = await resp.json()  
        embed = discord.Embed(title="Random Dog 🐶", color=0x4286F4)
        embed.set_image(url=json["message"])
        await ctx.send(embed=embed)

    @commands.command(name="bird", aliases=["birb", "ave"])
    async def bird(self, ctx):
        """Get a random birb image."""
        url = "http://random.birb.pw/tweet"
        imgURL = "https://random.birb.pw/img/"
        async with self.bot.session.get(url) as resp:
            imgID = await resp.text()
        embed = discord.Embed(title="Random Bird 🐦")
        embed.set_image(url=f"{imgURL}{imgID}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Animals(bot))
