from discord.ext import commands
import discord
import asyncio

class TagName(commands.clean_content):
    def __init__(self, *, lower=False):
        self.lower = lower
        super().__init__()

    async def convert(self, ctx, argument):
        converted = await super().convert(ctx, argument)
        lower = converted.lower().strip()

        if not lower:
            raise commands.BadArgument('Missing tag name.')

        if len(lower) > 100:
            raise commands.BadArgument('Tag name is a maximum of 100 characters.')

        first_word, _, _ = lower.partition(' ')

        # get tag command.
        root = ctx.bot.get_command('tag')
        if first_word in root.all_commands:
            raise commands.BadArgument('This tag name starts with a reserved word.')

        return converted if not self.lower else lower

class Tags:

    def __init__(self, bot):
        self.bot = bot

    async def get_tag(self, userID, name):
        document = await self.bot.db.tags.find_one({"_id": userID})
        if document is None:
            return False
        try:
            content = document["tags"][name]["content"]
        except KeyError:
            return False
        return content

    async def increaseTagUse(self, userID, name):
        document = await self.bot.db.tags.find_one({"_id": userID})
        document["tags"][name]["uses"] += 1
        await self.bot.db.tags.replace_one({"_id": userID}, document)

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, name: TagName(lower=True)):
        """Allows you to tag text for later retrieval.
        If a subcommand is not called, then this will search the tag database
        for the tag requested.
        """
        try:
            tag = await self.get_tag(ctx.author.id, name)
        except RuntimeError as e:
            return await ctx.send(e)
        if not tag:
            return await ctx.send("You don't have a tag with that name.")
        await ctx.send(tag)
        await self.increaseTagUse(ctx.author.id, name.lower())

    @tag.command(aliases=['add'])
    async def create(self, ctx, name: TagName, *, content: commands.clean_content):
        """Creates a new tag owned by you.
        This tag is server-specific and cannot be used in other servers.
        For global tags that others can use, consider using the tag box.
        Note that server moderators can delete your tag.
        """
        document = await self.bot.db.tags.find_one({"_id": ctx.author.id})
        if document is None:
            documentStructure = {
                "_id": ctx.author.id,
                "tags": {}
            }
            documentStructure["tags"][name.lower()] = {
                "content": content,
                "uses": 0
            }
            await self.bot.db.tags.insert_one(documentStructure)
            return await ctx.send(f"Created a tag called {name}.")
        if name.lower() in document["tags"]:
            return await ctx.send("The tag already exists.")
        document["tags"][name.lower()] = {
            "content": content,
            "uses": 0
        }
        await self.bot.db.tags.replace_one({"_id": ctx.author.id}, document)
        await ctx.send(f"Created a tag called {name}.")

    @tag.command(ignore_extra=False)
    async def make(self, ctx):
        """Interactive makes a tag for you.
        This walks you through the process of creating a tag with
        its name and its content. This works similar to the tag
        create command.
        """
        await ctx.send('What should the new tag name be?')
        converter = TagName()
        original = ctx.message

        def check(msg):
            return msg.author == ctx.author and ctx.channel == msg.channel
        try:
            name = await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send('Tag creation was cancelled due to long time of inactivity.')

        try:
            ctx.message = name
            name = await converter.convert(ctx, name.content)
        except commands.BadArgument as e:
            return await ctx.send(f'{e}. Redo the command "{ctx.prefix}tag make" to retry.')
        finally:
            ctx.message = original

        document = await self.bot.db.tags.find_one({"_id": ctx.author.id})
        if document is None:
            document = {
                "_id": ctx.author.id,
                "tags": {}
            }
        if name.lower() in document["tags"]:
            return await ctx.send("The name is already in use.")

        await ctx.send(f'So the name is {name}. What about the tag\'s content?')
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=300.0)
        except asyncio.TimeoutError:
            return await ctx.send('Tag creation cancelled due to long time of inactivity.')

        if msg.content:
            clean_content = await commands.clean_content().convert(ctx, msg.content)
        else:
            clean_content = msg.content
        if msg.attachments:
            clean_content = f'{clean_content}\n{msg.attachments[0].url}'

        await ctx.invoke(self.create, name=name, content=clean_content)

    @tag.command()
    async def edit(self, ctx, name: TagName(lower=True), *, content: commands.clean_content):
        """Modifies an existing tag that you own."""
        document = await self.bot.db.tags.find_one({"_id": ctx.author.id})
        if document is None:
            return await ctx.send("You don't have any tags.")
        lower = name.lower()
        document["tags"][lower]["content"] = content
        await self.bot.db.tags.replace_one({"_id": ctx.author.id}, document)
        await ctx.send(f"Tag `{name}` was successfully edited.")

    @tag.command(aliases=['delete'])
    async def remove(self, ctx, *, name: TagName(lower=True)):
        """Removes a tag that you own."""
        document = await self.bot.db.tags.find_one({"_id": ctx.author.id})
        if document is None:
            return await ctx.send("You have no tags.")
        document["tags"].pop(name, None)
        await self.bot.db.tags.replace_one({"_id": ctx.author.id}, document)
        await ctx.send(f"Successfully deleted `{name}`.")

    @tag.command(name='list')
    async def _list(self, ctx):
        """Lists all the tags that belong to you."""
        document = await self.bot.db.tags.find_one({"_id": ctx.author.id})
        if document is None:
            return await ctx.send("You have no tags.")
        counter = 0
        basestr = f"**{ctx.author.name}'s Tags** : \n```"
        if len(document["tags"].keys()) == 0:
            return await ctx.send("You have no tags.")
        for i in document["tags"].keys():
            counter += 1
            basestr += f"{counter}] {i}\n"
        basestr += "```"
        await ctx.send(basestr)


def setup(bot):
    bot.add_cog(Tags(bot))