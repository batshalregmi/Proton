import urllib.parse
import psutil
from platform import python_version
from discord.ext import commands
import discord

class Misc:

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()

    @commands.command(name="country")
    async def _country(self, ctx, *, name: str = None):
        """Shows a countries information, by name."""
        if name is None:
            return
        query = urllib.parse.quote(name)
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

    @commands.command(name="pypi")
    async def _pypi(self, ctx, *, name: str = None):
        """Search packages on PyPI."""
        if name is None:
            await ctx.send("Please state a package to search.")
            return
        key = self.bot.LibrariesIO
        base_url = "https://libraries.io/api/pypi/"
        query = base_url + name
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
    bot.add_cog(Misc(bot))