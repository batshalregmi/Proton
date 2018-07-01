async def uploadHastebin(ctx, text: str) -> str:
    """Uploads some text to hastebin and returns the URL."""
    async with ctx.bot.session.post("https://hastebin.com/documents", data=text.encode("utf-8")) as post:
        json = await post.json()
    return f"https://hastebin.com/{json['key']}"