import asyncio
import datetime
import discord
from discord.ext import commands
from discord.ext.commands import Bot


class VoteBot(commands.Cog):

    bot:Bot

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def poll(self, ctx, duration:int, question, *options):
        duration_hour = int(duration) * 60 *60
        final_datetime = datetime.datetime.now() + datetime.timedelta(hours=duration)
        end_datetime = final_datetime.strftime("%b %d, %Y, %I:%M %p")
        if len(options) <= 1:
            await ctx.send('You need atleast two option to create a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot create a poll with more than 10 options!')
            return
        if len(options) == 2 and options[0] == 'Yes' and options[1] == 'No':
            reactions = ['✅', '❌']
        elif len(options) == 2 and options[0] == 'No' and options[1] == 'Yes':
            reactions = ['❌', '✅']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']


        # Creating the poll fields and details
        description = []
        for i, option in enumerate(options):
            description += '> {} {}\n\n'.format(reactions[i], option)
        texts = ''.join(description)
        embed = discord.Embed(colour= discord.Color.random(),title=question, description=texts)
        file = discord.File("assets\Venatus_Dark_withbg.png", filename="Venatus_Dark_withbg.png")
        embed.set_thumbnail(url="attachment://Venatus_Dark_withbg.png")
        embed.add_field(name='\nPoll will end on `{}`'.format(end_datetime), value='', inline=False)
        embed.add_field(name='', value='`{}` created the poll.'.format(ctx.author), inline=False)
        react_message = await ctx.channel.send(embed=embed, view = None, file=file)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)


        await asyncio.sleep(duration_hour)  # Wait for the duration of the poll 

        # Get the poll results
        message = await ctx.channel.fetch_message(react_message.id)
        results = {}
        for reaction in message.reactions:
            if str(reaction.emoji) in reactions[:len(options)]:
                # Subtract the bot's own reaction
                results[reactions.index(str(reaction.emoji))] = reaction.count - 1
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        # Create the poll results message
        result_description = []
        for i, (option_index, count) in enumerate(sorted_results):
            result_description += '> {}. {} - {} vote{}\n\n'.format(
                i+1, options[option_index], count, 's' if count != 1 else '')
        res = ''.join(result_description)
        result_embed = discord.Embed(colour=discord.Color.random(), title='Poll Results: ' + question, description=res)
        file = discord.File("assets\Venatus_Dark_withbg.png", filename="Venatus_Dark_withbg.png")
        result_embed.set_thumbnail(url="attachment://Venatus_Dark_withbg.png")
        await ctx.channel.send(embed=result_embed, file=file, view=None)

        # Disable reactions on the poll message after the poll ends
        for reaction in message.reactions:
            await reaction.clear()


async def setup(bot):
    await bot.add_cog(VoteBot(bot))