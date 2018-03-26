from io import BytesIO
import discord


class Member:

    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        if member.guild is None:
            return
        #image = await self.bot.idiotic.welcome(avatar=member.avatar_url_as(format="png", static_format="png"), is_bot=str(member.bot).lower(), usertag=f"{member.name}#{member.discriminator}", guild=f"{member.guild.name}#{len(member.guild.members)}")
        #await channel.send(file=discord.File(BytesIO(image), f"Welcome {member.name}.png"))
        

def setup(bot):
    bot.add_cog(Member(bot))