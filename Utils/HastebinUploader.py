class Uploader:

    def __init__(self, bot):
        self.bot = bot

    async def uploadText(self, text):
        async with self.bot.session.post("https://hastebin.com/documents", data=text.encode("utf-8")) as post:
            json = await post.json()
            return f"https://hastebin.com/{json['key']}"