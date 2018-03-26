import os
import sys
import platform
import psutil
from discord.ext import commands
import discord
import json
import urllib.parse


class Information():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sinfo","ginfo"], name="serverinfo")
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """Shows information about the server"""
        guild = ctx.guild
        online = len([m.status for m in guild.members if (m.status == discord.Status.online) or (m.status == discord.Status.idle)])
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = "Since {}. That's over {} days ago!".format(guild.created_at.strftime('%d %b %Y %H:%M'), passed)
        data = discord.Embed(title='Server Information', description=created_at, colour=0x2CACD5)
        data.add_field(name='Server Name', value=guild.name, inline=True)
        data.add_field(name="Server Region", value=guild.region.title(), inline=True)
        data.add_field(name='Members', value=guild.member_count, inline=True)
        data.add_field(name='Server ID', value=guild.id, inline=True)
        data.add_field(name='Server Owner', value=str(guild.owner), inline=True)
        data.add_field(name='Roles', value=len(guild.roles), inline=True)
        data.add_field(name='Members Online', value=online, inline=True)
        if guild.icon_url:
            data.set_author(name=guild.name, icon_url=guild.icon_url)
        else:
            data.set_author(name=guild.name)
        await ctx.send(embed=data)

    @commands.command(aliases=["uinfo", "user"], name="userinfo")
    async def userinfo(self, ctx):
        """Displays information about a user."""
        if len(ctx.message.mentions) == 0:
            user = ctx.author
        else:
            if ctx.guild == None:
                await ctx.send("You can't use the mentions feature in DM.")
                return
            else:
                user = ctx.message.mentions[0]
        user_status = user.status
        if str(user.name) == str(user.nick):
            user_nick = 'No Nickname.'
        else:
            user_nick = user.nick
        user_status = str(user_status)
        if user_status == 'dnd':
            user_status = 'Do Not Disturb'
        else:
            user_status = user_status.title()
        data = discord.Embed(title='User Information', colour=0x2CACD5)
        data.add_field(name='User Name', value=user.name, inline=True)
        data.add_field(name='Nickname', value=user_nick, inline=True)
        data.add_field(name='User ID', value=user.id, inline=True)
        data.add_field(name='User Discrim', value="#" + str(user.discriminator), inline=True)
        data.add_field(name='Is User Bot', value=user.bot, inline=True)
        data.add_field(name='Account Created At', value="Since {}".format(user.created_at.strftime('%d %b %Y %H:%M')), inline=True)
        data.add_field(name='Status', value=user_status, inline=True)
        data.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=data)

    @commands.command(name="stats")
    async def stats(self, ctx):
        """Shows some information about the bot."""
        process = psutil.Process(os.getpid())
        memUsed = process.memory_info()[0] / float(2 ** 20)
        total_channels = 0
        total_users = len(self.bot.users)
        for traversal in self.bot.guilds:
            total_channels = total_channels + len(traversal.channels)
        os_gen_name = platform.system()
        if os_gen_name == "Linux":
            os_name_temp = platform.linux_distribution()
            os_name = str(os_name_temp[0]).title() + " " + str(str(os_name_temp[1]).split("/")[0]).title()
        elif os_gen_name == "Windows":
            os_name = "Windows"+ " " + str(platform.version()) + " " + str(platform.architecture)[0]
        PyVersion = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2])
        stats = discord.Embed(title="Bot Statistics", color=0x2CACD5)
        stats.add_field(name="Memory Usage", value="{} MB".format(memUsed), inline=True)
        stats.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        stats.add_field(name="Channels", value=total_channels, inline=True)
        stats.add_field(name="Users", value=total_users, inline=True)
        stats.add_field(name="Discord.Py", value="v{}".format(discord.__version__), inline=True)
        stats.add_field(name="Python", value="v{}".format(PyVersion), inline=True)
        stats.add_field(name="OS (Generic)", value=os_name, inline=True)
        stats.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=stats)

    
    @commands.command(name="country", aliases=["UN"])
    async def country(self, ctx, *, args=None):
        """Shows a countries information, by name."""
        if args is None:
            return
        query = urllib.parse.quote(args)
        base_url = f"https://restcountries.eu/rest/v2/name/{query}?fullText=true"
        async with self.bot.session.get(base_url) as response:
            if response.status != 200:
                await ctx.send("Invalid country name.")
                return
            response = await response.json()
            flag = "https://api.backendless.com/2F26DFBF-433C-51CC-FF56-830CEA93BF00/473FB5A9-D20E-8D3E-FF01-E93D9D780A00/files/CountryFlagsPng/"
            flag = flag + response[0]["alpha3Code"].lower() + ".png"
            name = response[0]["name"] + " (" + response[0]["alpha3Code"] + ") " + ":flag_" + response[0]["alpha2Code"].lower() + ":"
            basic = "Capital : " + "**" + response[0]["capital"] + "**\n"
            basic = basic + "Region : " + "**" + response[0]["region"] + "**\n"
            basic = basic + "Sub-Region : " + "**" + response[0]["subregion"] + "**\n"
            basic = basic + "Demonym : " + "**" + response[0]["demonym"] + "**\n"
            basic = basic + "Regional Name : " + "**" + response[0]["nativeName"] + "**\n"

            more = "Population : " + "**" + str(response[0]["population"]) + " people**\n"
            more = more + "Area : " + "**" + str(response[0]["area"]) + " sq Km**\n"
            more = more + "Main Timezone : " + "**" + response[0]["timezones"][0] + "**\n"

            currency = response[0]["currencies"][0]["name"] + " (" + response[0]["currencies"][0]["symbol"] + ")"
            
            extend = "Currency : " + "**" + currency + "**\n"
            extend = extend + "Official Languages : " + "**" + response[0]["languages"][0]["name"]
            extend = extend + " (" + response[0]["languages"][0]["nativeName"] + ")"
            if len(response[0]["languages"]) > 1:
                extend = extend + ", " + response[0]["languages"][1]["name"] + " (" + response[0]["languages"][1]["nativeName"] + ")**\n"
            else:
                extend = extend + "**\n"
            cn_embed = discord.Embed(title=name, colour=0x2CACD5)
            cn_embed.set_thumbnail(url=flag)
            cn_embed.add_field(name="❯❯ General Information", value=basic, inline=True)
            cn_embed.add_field(name="❯❯ More Information", value=more, inline=True)
            cn_embed.add_field(name="❯❯ Extended Information", value=extend, inline=False)
            cn_embed.set_footer(icon_url=self.bot.user.avatar_url, text="Powered by RestCountries API.")
            await ctx.send(embed=cn_embed)

    @commands.command()
    async def pypi(self, ctx, *, args=None):
        """Search packages on PyPI."""
        if args is None:
            await ctx.send("Please state a package to search.")
            return
        with open("Configuration/general.json") as read:
            key = json.load(read)["API"]["LibrariesIO"]
        base_url = "https://libraries.io/api/pypi/"
        query = base_url + args
        params = {"api_key" : key}
        async with self.bot.session.get(query, params=params) as response:
            if response.status != 200:
                await ctx.send("Not a valid package or teh service may be busy.")
                return
            details = await response.json()
            if len(details["normalized_licenses"]) == 0:
                licensex = "None"
            else:
                licensex = details["normalized_licenses"][0]
            if len(details["repository_url"]) == 0:
                authorx = "--------"
            else:
                authorx = details["repository_url"].split("/")[3].title()
            emb = discord.Embed(title=details["name"], description=details["description"], colour=0x2CACD5)
            vb = "**Latest Release** : " + str(details["latest_release_number"]) + "\n**"
            vb = vb + "License** : " + licensex + "\n**"
            vb = vb + "Author** : " + authorx + "\n**"
            vb = vb + "Download from PyPI** : [" + details["name"]+ "](" + details["package_manager_url"] + ")"
            emb.add_field(name="Details", value=vb)
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Information(bot))
