from discord.ext import commands
import discord
from lottery.controller import LotteryController

from settings import *


class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == int(DISCORD_WEBHOOK_LOTTERY_ID) and message.channel.id == 705701500881731605:
            dc = LotteryController()
            numbers = [int(x) for x in message.content.split(',')]
            dc.save(numbers)
            results = dc.get_drawing_results()
            embed = discord.Embed()
            embed.add_field(name="6 Correct", value=results['6'])
            embed.add_field(name="5 Correct", value=results['5'])
            embed.add_field(name="4 Correct", value=results['4'])
            embed.add_field(name="3 Correct", value=results['3'])
            embed.add_field(name="2 Correct", value=results['2'])
            await message.channel.send(embed=embed)

    @commands.group()
    async def lottery(self, ctx):
        ctx.lottery_con = LotteryController()

    @lottery.command(name="last")
    async def lottery_last(self, ctx):
        last_drawing = ctx.lottery_con.get_last_drawing()
        await ctx.send("Letzte Zeichnung: %s " % last_drawing.numbers_as_string())

    @lottery.command(name="next")
    async def lottery_next(self, ctx):
        pass

    @lottery.group(name="tickets")
    async def lottery_tickets(self, ctx):
        c = self.bot.get_command("Lottoscheine kosten")
        await ctx.invoke(c)

    @lottery_tickets.command(name="list")
    @commands.dm_only()
    async def lottery_tickets_list(self, ctx):
        embed = discord.Embed()
        for t in ctx.lottery_con.get_my_drawings(ctx.author):
            embed.add_field(
                name="Ticket", value=t.numbers_as_string(), inline=False)
        await ctx.send(embed=embed)

    @lottery_tickets.command(name="Kosten")
    async def lottery_tickets_costs(self, ctx):
        await ctx.send("Ein Ticket kostet 5 CR.")

    @lottery.command(name="beitreten")
    @commands.dm_only()
    async def lottery_join(self, ctx, *numbers: int):
        if len(numbers) != 6:
            await ctx.send("Wir brauchen sechs eindeutige Zahlen!")
            return

        duplicates = False
        out_of_bounds = False

        for n in numbers:
            if numbers.count(n) > 1:
                duplicates = True
            if n > 49 or n < 1:
                out_of_bounds = True

        if duplicates:
            await ctx.send("Sie benötigen 6 eindeutige Nummern, bitte wiederholen Sie keine Nummer!")
            return

        if out_of_bounds:
            await ctx.send("Sie können nur 6 eindeutige Zahlen zwischen 1 und 49 auswählen")
            return
        numbers = sorted(numbers)
        ctx.lottery_con.save(numbers, ctx.author)
        await ctx.send("Ihr Spielschein hat an der Lotterie teilgenommen.")


def setup(bot):
    bot.add_cog(Lottery(bot))
