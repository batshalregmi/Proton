import os
import json
import aiohttp
from discord.ext import commands
import discord
import motor.motor_asyncio


with open("Configuration/general.json") as read:
    settings = json.load(read)

Cogs = []

for i in os.listdir(settings["commandsDir"]):
    if i.endswith(".py"):
        Cogs.append(f'{settings["commandsDir"]}.{i.replace(".py", "")}')

for i in os.listdir(settings["eventsDir"]):
    if i.endswith(".py"):
        Cogs.append(f'{settings["eventsDir"]}.{i.replace(".py", "")}')


class Proton(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix=settings["core"]["prefix"], description=settings["core"]["description"])
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.DBClient = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.db = self.DBClient["proton"]
        self.guildSettings = self.db["guilds"]
        for extension in Cogs:
            try:
                self.load_extension(extension)
            except Exception:
                print(f'Failed to load extension {extension}.')

    async def on_ready(self):
        print(f'Ready: {self.user} (ID: {self.user.id}) (Guilds : {len(self.guilds)})')

    def run(self):
        super().run(settings["token"], reconnect=True)
    
    async def close(self):
        await super().close()
        await self.session.close()
        self.DBClient.close()
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(error)