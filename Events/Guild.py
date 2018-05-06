class Guild:

    def __init__(self, bot):
        self.bot = bot
    
    async def on_guild_join(self, guild):
        guild_create = {
            "_id": guild.id,
            "userLogEnabled": False,
            "userLogChannel": None,
            "userLogType": 1,
            "prefix": "$"
        }
        await self.bot.db.guilds.insert_one(guild_create)
        
    async def on_guild_remove(self, guild):
        await self.bot.db.guilds.delete_one({"_id": guild.id})


def setup(bot):
    bot.add_cog(Guild(bot))
