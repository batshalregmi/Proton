from discord.ext import commands
import discord
from datetime import datetime


class Admin:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="settings", aliases=["set"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx, *, args=None):
        """Edit your guilds's settings."""
        if args is None:
            guildset = await self.bot.db.guilds.find_one({'_id': ctx.message.guild.id})
            basestr = f"***{ctx.message.guild.name}'s*** Settings : \n```asciidoc\n== UserLog ==\n\t"
            basestr = basestr + ":: userLogEnabled : {}\n\t".format(guildset["userLogEnabled"])
            basestr = basestr + ":: userLogChannel : {}\n\t".format(guildset["userLogChannel"])
            basestr = basestr + ":: userLogType : {}\n".format(guildset["userLogType"])
            basestr = basestr + "== Core ==\n\t:: prefix : {}\n```".format(guildset["prefix"])
            await ctx.send(basestr)
        elif args.split(" ")[0] == "edit":
            try:
                keyToEdit = args.split(" ")[1]
                valueToEdit = args.split(" ")[2]
                if valueToEdit == "True":
                    valueToEdit = True
                elif valueToEdit == "False":
                    valueToEdit = False
                else:
                    try:
                        valueToEdit = int(valueToEdit)
                    except ValueError:
                        pass
            except IndexError:
                await ctx.send("Either key to edit or the value to change is not provided.")
            guildset = await self.bot.db.guilds.find_one({'_id': ctx.message.guild.id})
            for i in guildset.keys():
                if keyToEdit == i:
                    guildset[i] = valueToEdit
                    await self.bot.db.guilds.replace_one({"_id": ctx.guild.id}, guildset)
                    if keyToEdit == "prefix":
                        self.bot.guildPrefixes[ctx.guild.id] = valueToEdit
                    return await ctx.send(f"Value of {i} set to {valueToEdit}.")
                else:
                    pass
            await ctx.send("The specified key is not found.")
    
    @commands.command(name="kick")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member = None, *, reason=None):
        """
        Kick a person from the guild.
        The reason should be provided after the mention or ID.
        like so -> <prefix>kick @somebody <reason>
        """
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
    async def ban(self, ctx, user: discord.Member = None, *, reason=None):
        """
        Ban a person from the guild.
        The reason should be provided after the mention or ID.
        like so -> <prefix>ban @somebody <reason>
        """
        if user is None:
            return await ctx.send("Please provide a valid Discord guild memeber!")
        try:
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f"Successfully banned `{user.name}` from `{ctx.guild.name}`.")
        except discord.Forbidden:
            await ctx.send(f"Could not ban `{user.name}`.")

def setup(bot):
    bot.add_cog(Admin(bot))