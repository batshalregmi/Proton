import sys
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import discord
from discord.ext import commands


class Owner:
    """
    Contains command that can be used to alter the state of the bot, and can be only used by the owner of the bot.
    """

    def __init__(self, bot):
        self.bot = bot
        self.last_result = None

    def cleanup_code(self, content):
        """Get code from Discord codeblocks."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

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
    async def _reload(self, ctx, *, module: str = None):
        """Reloads a module."""

        if module is None:
            return await ctx.send("No module name provided.")
        module = f"Commands.{module}"
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            print(e)
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

    @commands.command(name="eval")
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str = None):
        """Execute arbitrary python code."""

        def _cleanup_code(content):
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])
            return content.strip('` \n')
        
        if body is None:
            return await ctx.send("No code provided.")

        env = {
            "bot": self.bot,
            "ctx": ctx,
            "message": ctx.message,
            "author": ctx.author,
            "guild": ctx.guild,
            "channel": ctx.channel,
            "_": self.last_result
        }
        env.update(globals())
        stdout = io.StringIO()
        to_compile = f"async def func():\n{textwrap.indent(_cleanup_code(body), '  ')}"

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        
        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
        

def setup(bot):
    bot.add_cog(Owner(bot))