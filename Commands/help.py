from collections import defaultdict
from datetime import datetime
from inspect import getdoc
import discord
from discord.ext import commands


class Help:
    """
    See information about other categories and commands.
    """

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

    async def _can_run(self, cmd, ctx):
        try:
            return await cmd.can_run(ctx)
        except Exception:
            return False

    async def BotEmbed(self, ctx):
        registeredCommands = list(self.bot.commands)
        plausibleCommands = [cmd for cmd in registeredCommands if (await self._can_run(cmd, ctx)) and not cmd.hidden]
        cogs_dict = defaultdict(list)
        for i in plausibleCommands:
            cogs_dict[i.cog_name].append(f"`{i.name}`")
        editedCogNames = "\n".join([f"• **{x}**" for x in sorted(list(cogs_dict.keys()), key=lambda c: c)])
        desc = f"Type `{ctx.prefix}help <category>` for detailed help about a particular category.\n{editedCogNames}"
        helpEmbed = discord.Embed(title=f"{self.bot.user.name}'s Command Categorys", description=desc, color=0x42F465)
        helpEmbed.set_footer(text=f"{self.bot.user.name} {datetime.utcnow().year}. Licensed under MIT license.", icon_url=self.bot.user.avatar_url)
        return helpEmbed

    async def CommandsEmbed(self, cmd, ctx):
        if not await self._can_run(cmd, ctx):
            return discord.Embed(title="Error!", description=f"The command you requested cannot be run here, or you don't have enough permissions.", color=0x42F465)
        info = f"""\U0001F4C3 | **Description of Command** | **__{cmd.qualified_name}__**
{cmd.help}

\U00002328 | **Command Usage**
`{ctx.prefix}{cmd.signature}`

\U0001F517 | **Aliases**
{", ".join(sorted(cmd.aliases, key=lambda c: c)) if cmd.aliases else None}

\U00002B07 **Subcommands**
{", ".join(["`{}`".format(x.qualified_name) for x in sorted(list(cmd.commands), key=lambda c: c.qualified_name)]) if isinstance(cmd, commands.Group) else None}"""
        return discord.Embed(title=f"{cmd.qualified_name} command", description=info, color=0x42F465)

    async def CategoryEmbed(self, cog, ctx):
        cog_name = cog.__class__.__name__
        cogCommands = sorted([x for x in list(self.bot.get_cog_commands(cog_name)) if (await self._can_run(x, ctx)) and not x.hidden], key=lambda c: c.name)
        if not cogCommands:
            return discord.Embed(title="Error!", description="You cannot run any commands present in the category.", color=0x42F465)
        cogHelp = "\n".join([f"**{x.name}:** `{x.help}`" for x in cogCommands])
        desc = f"Type `{ctx.prefix}help <command>` for detailed help about a particular command.\n```{getdoc(cog)}```\n{cogHelp}"
        return discord.Embed(title=f"{cog_name}'s commands", description=desc, color=0x42F465)

    @commands.command(name="help", aliases=["h", "cmds"])
    async def _help(self, ctx, *, commandName: str = None):
        """Shows this message."""
        if commandName is None:
            embed = await self.BotEmbed(ctx)
            return await ctx.send(embed=embed)
        entity = self.bot.get_cog(commandName) or self.bot.get_command(commandName)
        if not entity:
            return await ctx.send("Category/Command not found.")
        if isinstance(entity, (commands.Command, commands.Group)):
            embed = await self.CommandsEmbed(entity, ctx)
            await ctx.send(embed=embed)
        else:
            embed = await self.CategoryEmbed(entity, ctx)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))