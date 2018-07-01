from discord.ext import commands
import discord
from datetime import datetime


class Admin:
    """
    Contains commands for administration of the guild.
    """

    def __init__(self, bot):
        self.bot = bot

    def generateSettings(self, guildSettings):
        paginator = commands.Paginator(prefix="```asciidoc")
        paginator.add_line("== Core ==")
        paginator.add_line(f"\t:: prefix : {guildSettings['prefix']}", empty=True)
        paginator.add_line("== User Log ==")
        paginator.add_line(f"\t:: userLogEnabled : {guildSettings['userLogEnabled']}")
        paginator.add_line(f"\t:: userLogType : {guildSettings['userLogType']}")
        paginator.add_line(f"\t:: userLogChannel : {guildSettings['userLogChannel']}")
        paginator.close_page()
        return paginator.pages

    @commands.group(name="settings", aliases=["set"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        """An interface for viewing and editting bot settings for your guild."""
        if ctx.invoked_subcommand is None:
            return await ctx.send(f"Please execute a valid subcommand, see `{ctx.prefix}help set` for more.")

    @settings.command(name="view")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _view(self, ctx):
        """View the settings of the guild."""
        guildset = await self.bot.db.guilds.find_one({'_id': ctx.message.guild.id})
        guildset.pop('_id', None)
        pages = await self.bot.loop.run_in_executor(None, self.generateSettings, guildset)
        if len(pages) > 1:
            pageLength = len(pages)
            embeds = []
            for i in pages:
                desc = f"To Edit a specific setting, do `{ctx.prefix}set edit [key] [value]`\n{i}"
                embed = discord.Embed(title=f"Page {pages.index(i) + 1} of {pageLength}. {self.bot.user.name} Settings Viewer.", 
                                        description=desc, color=0x42F465)
                embeds.append(embed)
            for i in embeds:
                await ctx.send(embed=i)
        else:
            info = f"To edit a specific setting, do `{ctx.prefix}set edit [key] [value]`.\n{pages[0]}"
            embed = discord.Embed(title=f"{ctx.message.guild.name}'s Settings: ", description=info, color=0x42F465)
            embed.set_footer(text=f"{self.bot.user.name} - {datetime.utcnow().year}.", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)

    @settings.command(name="edit")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def _edit(self, ctx, key: str = None, value: str = None):
        """Edit the settings of your guild."""
        if key is None or value is None:
            return await ctx.send("Either the key or value parameter or both are empty.")
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        else:
            try:
                value = int(value)
            except ValueError:
                pass
        guildset = await self.bot.db.guilds.find_one({'_id': ctx.message.guild.id})
        guildset.pop("_id")
        for i in guildset.keys():
            if key == i:
                guildset[i] = value
                guildset["_id"] = ctx.guild.id
                await self.bot.db.guilds.replace_one({"_id": ctx.guild.id}, guildset)
                if key == "prefix":
                    self.bot.guildPrefixes[ctx.guild.id] = value
                return await ctx.send(f"Value of `{i}` set to `{value}`.")
            else:
                pass
        await ctx.send("The specified key is not found.")


    @commands.command(name="kick")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member = None, *, reason=None):
        """Kick a person from the guild."""
        if user is None:
            return await ctx.send("Please provide a valid Discord guild memeber!")
        try:
            await ctx.guild.kick(user, reason=reason)
            await ctx.send(f"Successfully kicked `{user.name}` from `{ctx.guild.name}`.")
        except discord.Forbidden:
            await ctx.send(f"Could not kick `{user.name}`.")

    @commands.command(name="ban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member = None, *, reason=None, days: int = 7):
        """Ban a person from the guild. Specify days after reason to delete the members messages. MAX is 7 days."""
        if user is None:
            return await ctx.send("Please provide a valid Discord guild memeber!")
        try:
            await ctx.guild.ban(user, reason=reason, delete_message_days=days)
            await ctx.send(f"Successfully banned `{user.name}` from `{ctx.guild.name}`.")
        except discord.Forbidden:
            await ctx.send(f"Could not ban `{user.name}`.")

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: int = None, *, reason=None):
        """Unban a person from the guild"""
        if user is None:
            return await ctx.send("Please provide the user's ID to unban him.")
        elif len(str(user)) > 18 or len(str(user)) < 18:
            return await ctx.send("Please provide a valid user's ID")
        try:
            await ctx.guild.unban(discord.Object(user), reason=reason)
            await ctx.send(f"Successfully unbanned the user.")
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send("Couldn't unban user.")

def setup(bot):
    bot.add_cog(Admin(bot))