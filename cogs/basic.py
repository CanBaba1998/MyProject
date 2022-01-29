from discord.ext import commands
import discord

from utils import text_to_owo, notify_user


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        print(ex)
        await ctx.send("Bitte überprüfen Sie mit !help die Verwendung dieses Befehls oder sprechen Sie mit Ihrem Administrator.")

    @commands.command(brief="Jede Nachricht an owo")
    async def owo(self, ctx):
        await ctx.send(text_to_owo(ctx.message.content))

    @commands.command(brief="Erstellt einen Einladungslink zum Kanal")
    @commands.guild_only()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=1)
        await ctx.send(link)

    @commands.command()
    async def poke(self, ctx, member: discord.Member = None):

        if member is not None:
            message = "%s hat dich gepiekst!!!!" % ctx.author.name
            await notify_user(member, message)
        else:
            await ctx.send("Bitte verwenden Sie @, um jemanden anzustupsen.")


def setup(bot):
    bot.add_cog(Basic(bot))
