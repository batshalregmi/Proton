import discord
from discord.ext import commands
import sys

class Owner:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["l"])
    @commands.is_owner()
    async def load(self, ctx, *, module):
        """Loads a module."""
        module = f"Commands.{module}"
        try:
            self.bot.load_extension(module)
        except Exception:
            await ctx.message.add_reaction("\N{NEGATIVE SQUARED CROSS MARK}")
        else:
            await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

    @commands.command(aliases=["u"])
    @commands.is_owner()
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        module = f"Commands.{module}"
        try:
            self.bot.unload_extension(module)
        except Exception:
            await ctx.message.add_reaction("\N{NEGATIVE SQUARED CROSS MARK}")
        else:
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @commands.command(name='reload', aliases=["r"])
    @commands.is_owner()
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        module = f"Commands.{module}"                
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception:
            await ctx.message.add_reaction("\N{NEGATIVE SQUARED CROSS MARK}")
        else:
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @commands.command(name='exit', aliases=["s", "shutdown"])
    @commands.is_owner()
    async def _exit(self, ctx):
        """Initiate shutdown of bot."""
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        await self.bot.close()

    @commands.command(name="dbregen")
    @commands.is_owner()
    async def dbregen(self, ctx):
        """Re-create DB entry of guild."""
        guild_create = {
            "_id": ctx.guild.id,
            "userLogEnabled": False,
            "userLogChannel": None,
            "userLogType": 1,
            "prefix": "$"
        }
        await self.bot.db.guilds.insert_one(guild_create)
        await ctx.send("DB entry regenerated.")

def setup(bot):
    bot.add_cog(Owner(bot))