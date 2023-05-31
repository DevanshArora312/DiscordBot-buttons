import discord
from discord.ext import commands
from discord.ext.commands import bot_has_permissions, has_permissions
import datetime


class Mod(commands.Cog):
    def __init__(self,client):
        self.client = client



    @commands.command(aliases=['purge'])
    async def clear(self, ctx, limit =1):
        if 0 < limit < 101:
            deleted = await ctx.channel.purge(limit= limit+1)
            await ctx.send(f"Deleted {(len(deleted)-1):,} messages.", delete_after = 2)
        else:
            await ctx.send("The limit provided is not within acceptable bounds.")




    @commands.command(aliases=['timeout'])
    @commands.has_any_role("Moderator", "Administrator", "Owner")
    async def mute(self, ctx, member:discord.Member, timelimit):

        if "s" in timelimit:
            gettime = timelimit.strip("s")
            if int(gettime) > 2419000:
                await ctx.send("The mute time amount cannot be bigger than 28 days")
            else:
                newtime = datetime.timedelta(seconds=int(gettime))
                await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                await ctx.send(f"Successfully muted {member.mention} for {timelimit[:-1]} seconds")

        elif "m" in timelimit:
            gettime = timelimit.strip("m")
            if int(gettime) > 40320:
                await ctx.send("The mute time amount cannot be bigger than 28 days")
            else:
                newtime = datetime.timedelta(minutes=int(gettime))
                await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                await ctx.send(f"Successfully muted {member.mention} for {timelimit[:-1]} minutes")


        elif "h" in timelimit:
            gettime = timelimit.strip("h")
            if int(gettime) > 672:
                await ctx.send("The mute time amount cannot be bigger than 28 days")
            else:
                newtime = datetime.timedelta(hours=int(gettime))
                await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                await ctx.send(f"Successfully muted {member.mention} for {timelimit[:-1]} hours")
                

        elif "w" in timelimit:
            gettime = timelimit.strip("w")
            if int(gettime)>4:
                await ctx.send("The mute time amount cannot be bigger than 4 weeks")
            else:
                newtime = datetime.timedelta(weeks = int(gettime))
                await member.edit(timed_out_until=discord.utils.utcnow()+newtime)
                await ctx.send(f"Successfully muted {member.mention} for {timelimit[:-1]} weeks")


async def setup(client):
    await client.add_cog(Mod(client))