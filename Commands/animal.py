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
        url = "http://shibe.online/api/birds"
        async with self.bot.session.get(url) as resp:
            json = await resp.json()
        embed = discord.Embed(title="Random Bird 🐦")
        embed.set_image(url=json[0])
        await ctx.send(embed=embed)

    @commands.command(name="cat", aliases=["kitten", "kitty"])
    async def cat(self, ctx):
        """Get a random cat image."""
        url = "http://shibe.online/api/cats"
        async with self.bot.session.get(url) as resp:
            json = await resp.json()
        embed = discord.Embed(title="Random Cat 🐱")
        embed.set_image(url=json[0])
        await ctx.send(embed=embed)

    @commands.command(name="shibe", aliases=["shiba", "inu"])
    async def shibe(self, ctx):
        """Get a random shiba inu dog image."""
        url = "http://shibe.online/api/shibes"
        async with self.bot.session.get(url) as resp:
            json = await resp.json()
        embed = discord.Embed(title="Random Shibe 🐕")
        embed.set_image(url=json[0])
        await ctx.send(embed=embed)
        
    @commands.command(name="fox")
    async def fox(self, ctx):
        """Get a random fox image."""
        url = "https://randomfox.ca/floof/"
        async with self.bot.session.get(url) as resp:
            json = await resp.json()
        embed = discord.Embed(title="Random Fox 🦊")
        embed.set_image(url=json["image"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Animals(bot))
