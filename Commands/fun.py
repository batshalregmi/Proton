import asyncio
import random
import discord
from discord.ext import commands
from Utils import TicTacToeLib
from Assets.DataLists import asciiFaces

class Fun:
    
    def __init__(self, bot):
        self.bot = bot 
        self.sessions = set()

    def _parseWin(self, user, automation):
        if automation == user:
            return None
        elif user == "rock":
            return True if automation == "scissor" else False
        elif user == "paper":
            return True if automation == "rock" else False
        else:
            return True if automation == "paper" else False

    @commands.command(name="tictactoe", aliases=["ttc"])
    @commands.guild_only()
    async def tictactoe(self, ctx, user: discord.Member = None):
        """Play a game of Tic Tac Toe with your friend!"""
        if user is None:
            return await ctx.send("Please specify whom you want to play tic tac toe with!")
        if user.bot:
            return await ctx.send("You can't play with bots.")
        #if user == ctx.author:
            #return await ctx.send("You can't challenge yourself!")
        if ctx.guild.id in self.sessions:
            return await ctx.send("A game is already being played in this server.")
        self.sessions.add(ctx.guild.id)
        desc = f"""{user.name}, you have been challenged by {ctx.author.name} to a round of Tic Tac Toe, will
you accept the challenge? Reply `y` for yes and `n` for no. This will terminate in `30 seconds`."""    
        embed = discord.Embed(title="Tic Tac Toe Challenge", description=desc)
        embedMessage = await ctx.send(user.mention, embed=embed)
        def check_msg(m):
            if ctx.channel == m.channel and user == m.author:
                if m.content.lower() == "y" or m.content.lower() == "n":
                    return True
            return False
        try:
            message = await self.bot.wait_for("message", timeout=30.0, check=check_msg)
        except asyncio.TimeoutError:
            return await ctx.send(f"{message.author.mention} took too long to respond, hence terminating.")
        if message.content == "y":
            await embedMessage.delete()
            winner = None
            player = (":o:", ctx.author)
            opp = (":x:", user)
            boardActual = TicTacToeLib.Board()
            def playerMessageCheck(msg):
                if msg.author == player[1] and msg.channel == ctx.channel:
                    if msg.content.isdigit():
                        if int(msg.content) <= 9 and int(msg.content) > 0:
                            if boardActual.checkMove(int(msg.content)):
                                return True
                return False
            def oppMessageCheck(msg):
                if msg.author == opp[1] and msg.channel == ctx.channel:
                    if msg.content.isdigit():
                        if int(msg.content) <= 9:
                            if boardActual.checkMove(int(msg.content)):
                                return True
                return False
            while True:
                if boardActual.isFull():
                    break
                await ctx.send(f"{player[1].mention}, it's your turn! You have 30 seconds to play a move, or you will lose.")
                await ctx.send(boardActual.printStr())
                try:
                    move = await self.bot.wait_for("message", timeout=30.0, check=playerMessageCheck)
                except asyncio.TimeoutError:
                    await ctx.send(f"{player[1].mention} took to long to play a move.")
                    winner = opp
                    break
                trueMove = int(move.content)
                boardActual.playMove(trueMove, player[0])
                if boardActual.checkWin(player[0]):
                    winner = player
                    break
                if boardActual.isFull():
                    break
                await ctx.send(f"{opp[1].mention}, it's your turn! You have 30 seconds to play a move, or you will lose.")
                await ctx.send(boardActual.printStr())
                try:
                    move = await self.bot.wait_for("message", timeout=30.0, check=oppMessageCheck)
                except asyncio.TimeoutError:
                    await ctx.send(f"{opp[1].mention} took to long to play a move.")
                    winner = player
                    break
                trueMove = int(move.content)
                boardActual.playMove(trueMove, opp[0])
                if boardActual.checkWin(opp[0]):
                    winner = opp
                    break
            if winner is None:
                await ctx.send(boardActual.printStr())
                await ctx.send("Alas, there was no winner, that means it's a tie, and that means you BOTH WIN!")
            else:
                await ctx.send(boardActual.printStr())
                await ctx.send(f"The winner is {winner[1].mention}! Great Moves! TEST: ({winner[0]})")
        else:
            await ctx.send(f"Challenge declined by {message.author.mention}.")
            await embedMessage.delete()
        self.sessions.remove(ctx.guild.id)
    
    @commands.command(name="rps")
    async def rps(self, ctx, move: str = None):
        """Play a turn of rock paper scissors with me.
           Valid moves are rock, paper, scissor (case insensitive).         
        """
        movesTuple = ("rock", "paper", "scissor")
        if move is None:
            return await ctx.send("Please specify your move!")
        elif not move.lower() in movesTuple:
            return await ctx.send(f"Invalid move, see `{ctx.prefix}help rps` for more.")
        rand = random.choice(movesTuple)
        res = await self.bot.loop.run_in_executor(None, self._parseWin, move.lower(), rand)
        if res is None:
            return await ctx.send(f"Alas, it's a TIE! `{move} == {rand}` 😉")
        if res:
            return await ctx.send(f"How could I even lose to you? `{move.lower()} > {rand}` 😕")
        await ctx.send(f"Haha, I won! `{rand} > {move.lower()}` 😄")

    @commands.command(name="cowsay")
    async def _cowsay(self, ctx, *, text: str = None):
        """Make a cow say what you want."""
        if text is None:
            return await ctx.send("Please provide some text to our cow!")
        URL = f"http://cowsay.morecode.org/say"
        async with self.bot.session.get(URL, params={"message": text, "format": "json"}) as resp:
            cowSays = await resp.json()
        if len(cowSays["cow"]) >= 2000:
            return await ctx.send("Our cow can't understand so much text at once, please give him some smaller text.")
        await ctx.send(f"```{cowSays['cow']}```")

    @commands.command(name="chuck", aliases=["chucknorris", "norris"])
    async def _chuckNorris(self, ctx):
        """Get a random Chuck Norris joke."""
        async with self.bot.session.get("http://api.icndb.com/jokes/random", params={"escape": "javascript"}) as resp:
            joke = await resp.json()
        embed = discord.Embed(title="Chuck Norris", description=joke["value"]["joke"], colour=0x36393E)
        embed.set_thumbnail(url="https://assets.chucknorris.host/img/avatar/chuck-norris.png")
        await ctx.send(embed=embed)
        
    @commands.command(name="asciiface", aliases=["ascii"])
    async def _ascii(self, ctx):
        """Get a random ASCII face."""
        randChoice = await self.bot.loop.run_in_executor(None, random.choice, asciiFaces.asciiFaceList)
        await ctx.send(randChoice)

def setup(bot):
    bot.add_cog(Fun(bot))