import asyncio

from discord.ext import commands
import discord
import datetime
from discord.ext.commands import has_permissions, MissingPermissions
from discord import app_commands

class Moderation(commands.Cog):

    def __int__(self,bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self, ctx):
        print("test")
        embed = discord.Embed(
            colour=discord.Colour.orange(),
            title="Map Selected",
            description="**Dust 2**"
        )
        # Add more detailed information about the map
        embed.add_field(name="Map Type", value="Bomb Defusal", inline=True)
        embed.add_field(name="Max Players", value="10", inline=True)
        # Set a footer with additional information
        embed.set_footer(text="CS:GO - Counter-Strike: Global Offensive")

        # Set a larger image within the embed
        embed.set_image(url="https://image.pngaaa.com/220/1552220-middle.png")
        await ctx.channel.send(embed=embed, view=None)
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, who: discord.Member, reason: str):
        print("kimk")

        try:
            await who.kick(reason=reason)
            embed = discord.Embed(colour=discord.Colour.red(), title="", description="")
            embed.add_field(name="Kicked:", value=f"""
            The user **{who}** has been kicked
            Reason = **{reason}**
            """, inline=True)
            await ctx.channel.send(embed=embed)
        except Exception as e:
            print(e)
            embed = discord.Embed(colour=discord.Colour.red(), title="Error", description=e)
            await ctx.channel.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, who: discord.Member, reason: str):
        print("bamn")

        try:
            await who.ban(reason=reason)
            embed = discord.Embed(colour=discord.Colour.red(), title="", description="")
            embed.add_field(name="Banned:", value=f"""
            The user **{who}** has been banned
            Reason = **{reason}**
            """, inline=True)
            await ctx.channel.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(colour=discord.Colour.red(), title="Error", description=e)
            await ctx.channel.send(embed=embed)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx, userid: str):
        print("unbamn")

        try:
            user = discord.Object(id=userid)
            await ctx.guild.unban(user)

            embed = discord.Embed(colour=discord.Colour.red(), title="", description="")
            embed.add_field(name="UnBanned:", value=f"""
            The user <@{userid}> has been unbanned
            """, inline=True)

            await ctx.channel.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(colour=discord.Colour.red(), title="Error", description=e)
            await ctx.channel.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Moderation(bot))