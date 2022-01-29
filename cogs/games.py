import random
from discord.ext import commands
import discord

from rps.model import RPS
from rps.parser import RockPaperScissorParser
from rps.controller import RPSGame

from hangman.controller import HangmanGame

from gaw.controller import GuessAWordGame


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="rock | paper | scissor")
    async def rps(self, ctx, user_choice: RockPaperScissorParser = RockPaperScissorParser(RPS.ROCK)):
        """
        Spielen Sie eine Partie Schere Stein, Papier

        Wählen Sie entweder Stein, Papier oder Schere und schlagen Sie den Bot

        Sie können keinen anderen Benutzer herausfordern. Nur Sie gegen den Bot!
        """
        game_instance = RPSGame()

        user_choice = user_choice.choice

        won, bot_choice = game_instance.run("asd")

        if won is None:
            message = "Es ist gleichstand! Beide wählten: %s" % user_choice
        elif won is True:
            message = "Du gewinnst: %s vs %s" % (user_choice, bot_choice)
        elif won is False:
            message = "Du Loser geh dich vergraben: %s vs %s" % (user_choice, bot_choice)

        await ctx.send(message)

    @commands.command()
    @commands.dm_only()
    async def hm(self, ctx, guess: str):
        player_id = ctx.author.id
        hangman_instance = HangmanGame()
        game_over, won = hangman_instance.run(player_id, guess)

        if game_over:
            game_over_message = "Du hast nicht gewonnen"
            if won:
                game_over_message = "Herzlichen Glückwunsch, du hast gewonnen!!"

            game_over_message = game_over_message + \
                " Das Wort war %s" % hangman_instance.get_secret_word()

            await hangman_instance.reset(player_id)
            await ctx.send(game_over_message)

        else:
            await ctx.send("Fortschritt: %s" % hangman_instance.get_progress_string())
            await ctx.send("Vermutung so weit: %s" % hangman_instance.get_guess_string())

    @commands.group()
    async def gaw(self, ctx):
        ctx.gaw_game = GuessAWordGame()

    @gaw.command(name="start")
    async def gaw_start(self, ctx, *members: discord.Member):
        guild = ctx.guild
        author = ctx.author
        players = list()
        for m in members:
            players.append(m)

        channel = await ctx.gaw_game.start_game(guild, author, players)
        if channel is None:
            await ctx.send("Sie haben bereits ein Spiel. Bitte schließen Sie es zuerst")
        else:
            game = ctx.gaw_game.fetch_game()
            await ctx.send("Habe Spaß! Bitte gehen Sie in den neuen Spielraum.")
            await channel.send(
                "Die erste Runde findet in der Kategorie: %s mit einer Wortlänge von %s statt" % (game.category, len(game.word)))

    @gaw.command(name="g")
    async def gaw_guess(self, ctx, guess: str):
        channel = ctx.channel
        author = ctx.author
        result, hint = ctx.gaw_game.guess(channel.id, guess)

        if result is None:
            await ctx.send("Du darfst in diesem Kanal nicht spielen!")
        elif result is True:
            await ctx.send("%s du hast gewonnen!" % author.name)
            # start new round
            ctx.gaw_game.new_round(channel)
            new_round = ctx.gaw_game.fetch_game()
            await channel.send(
                "Neue Runde! Kategorie: %s mit einer Wortlänge von %s" % (new_round.category, len(new_round.word)))
        elif result is False and hint != "":
            await ctx.send("%s sehr nah!" % author.name)

    @gaw.command(name="end")
    async def gaw_end(self, ctx):
        guild = ctx.guild
        channel = ctx.channel
        await ctx.gaw_game.destroy(guild, channel.id)


def setup(bot):
    bot.add_cog(Games(bot))
