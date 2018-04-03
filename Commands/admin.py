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
            basestr = basestr + ":: userLogType : {}\n```".format(guildset["userLogType"])
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
                    return await ctx.send(f"Value of {i} set to {valueToEdit}.")
                else:
                    pass
            await ctx.send("The specified key is not found.")
            

def setup(bot):
    bot.add_cog(Admin(bot))