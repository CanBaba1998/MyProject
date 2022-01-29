from discord.ext import commands
import discord

from utils import mods_or_owner


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @mods_or_owner()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, reason: str = "Weil du schlecht warst. Wir haben dich gekickt."):
        if member is not None:
            await ctx.guild.kick(member, reason=reason)
        else:
            await ctx.send("Bitte geben Sie den zu kickenden Benutzer per Erwähnung an mit @")

    @commands.command()
    @mods_or_owner()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, reason: str = "Weil du unartig bist. Wir haben dich gesperrt."):
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
        else:
            await ctx.send("Bitte geben Sie den zu bannenden Benutzer per Erwähnung an mit @")

    @commands.command()
    @mods_or_owner()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: str = "", reason: str = "Du wurdest entbannt. Die Zeit ist um. Benimm dich bitte"):
        if member == "":
            await ctx.send("Bitte geben Sie den Benutzernamen als Text an")
            return

        bans = await ctx.guild.bans()
        for b in bans:
            if b.user.name == member:
                await ctx.guild.unban(b.user, reason=reason)
                await ctx.send("Benutzer wurde entbannt")
                return
        await ctx.send("Der Benutzer wurde nicht in der Sperrliste gefunden.")


def setup(bot):
    bot.add_cog(Moderator(bot))
