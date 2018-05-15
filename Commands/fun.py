import asyncio
import re
import discord
from discord.ext import commands
from Utils import TicTacToeLib

class Fun:
    
    def __init__(self, bot):
        self.bot = bot 
        self.sessions = set()

    @commands.command(name="tictactoe", aliases=["ttc"])
    async def tictactoe(self, ctx, user: discord.Member = None):
        """Play a game of Tic Tac Toe with your friend!"""
        if user is None:
            return await ctx.send("Please specify whom you want to play tic tac toe with!")
        if user.bot:
            return await ctx.send("You can't play with bots.")
        if user == ctx.author:
            return await ctx.send("You can't challenge yourself!")
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
        


def setup(bot):
    bot.add_cog(Fun(bot))