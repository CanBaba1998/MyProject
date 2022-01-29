import random

from discord.ext import commands


class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Gibt eine Zufallszahl zwischen 1 und 100 aus")
    async def roll(self, ctx):
        n = random.randrange(1, 101)
        await ctx.send(n)

    @commands.command(brief="Zufallszahl zwischen 1 und 6")
    async def dice(self, ctx):
        n = random.randrange(1, 6)
        await ctx.send(n)

    @commands.command(brief="Entweder Kopf oder Zahl")
    async def coin(self, ctx):
        n = random.randint(0, 1)
        await ctx.send("Heads" if n == 1 else "Tails")


def setup(bot):
    bot.add_cog(Gamble(bot))
