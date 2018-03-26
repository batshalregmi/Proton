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
            userLog = guildset["userLog"]
            basestr = f"***{ctx.message.guild.name}'s*** Settings : \n```asciidoc\n== UserLog ==\n\t"
            basestr = basestr + ":: userLogEnabled : {}\n\t".format(userLog["userLogEnabled"])
            basestr = basestr + ":: userLogChannel : {}\n\t".format(userLog["userLogChannel"])
            basestr = basestr + ":: userLogType : {}\n```".format(userLog["userLogType"])
            await ctx.send(basestr)
        elif args.split(" ")[0] == "edit":
            try:
                keyToEdit = args.split(" ")[1]
                valueToEdit = args.split(" ")[2]
            except IndexError:
                await ctx.send("Either key to edit or the value to change is not provided.")
            guild_settings = {
                "userLog": {
                    "userLogEnabled": False,
                    "userLogChannel": None,
                    "userLogType": 1
                }
            }
            for i in guild_settings.keys():
                if keyToEdit in guild_settings[i]:
                    guild_settings[i][keyToEdit] = valueToEdit
                    guild_settings["_id"] = ctx.message.guild.id
                    await self.bot.db.guilds.replace_one({'_id': ctx.message.guild.id}, guild_settings)
                    await ctx.send(f"Value of key `{keyToEdit}`` successfully changed to `{valueToEdit}`.")
                    return
                else:
                    pass
            await ctx.send("The specified key is not found.")
            

def setup(bot):
    bot.add_cog(Admin(bot))