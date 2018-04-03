from io import BytesIO
import discord
from Utils import ImageClient
import functools


class Member:

    def __init__(self, bot):
        self.bot = bot
        self.imageClient = ImageClient.ImageClient(bot)

    async def on_member_join(self, member):
        if member.guild is None:
            return
        settings = await self.bot.db["guilds"].find_one({'_id': member.guild.id})
        if not settings["userLogEnabled"]:
            return
        if settings["userLogType"] == 3:
            avatar = await self.imageClient.getAvatar(member, size=256)
            func = functools.partial(self.imageClient.welcomeImage, avatar, member.name, member.discriminator, member.guild)
            image = await self.bot.loop.run_in_executor(None, func)
            file = discord.File(fp=image, filename=f"Welcome {member.name}.png")
            channel = self.bot.get_channel(settings["userLogChannel"])
            await channel.send(file=file)

    async def on_member_remove(self, member):
        if member.guild is None:
            return
        settings = await self.bot.db["guilds"].find_one({'_id': member.guild.id})
        if not settings["userLogEnabled"]:
            return
        if settings["userLogType"] == 3:
            avatar = await self.imageClient.getAvatar(member, size=256)
            func = functools.partial(self.imageClient.goodbyeImage, avatar, member.name, member.discriminator)
            image = await self.bot.loop.run_in_executor(None, func)
            file = discord.File(fp=image, filename=f"Goodbye {member.name}.png")
            channel = self.bot.get_channel(settings["userLogChannel"])
            await channel.send(file=file)


def setup(bot):
    bot.add_cog(Member(bot))