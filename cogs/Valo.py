import discord
from discord.ui import Button,View
from discord.ext import commands

class ValoVeto(discord.ui.View):
    #This is a button view class which is called later in code

    def __init__(self,cap1,cap2):
        super().__init__()
        ##~~~~~~~~~~~~~DECLARE ALL VARIABLES HERE USING self.varName = varValue ~~~~~~~~~~~~~~~~~~~~~~~~~~##
        self.value=None
        self.cap1 = cap1
        self.cap2 = cap2
        self.mapleft = 7
        self.votingTurn=0 #odd means cap1 and even means cap2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Veto Buttons~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @discord.ui.button(label="Breeze" ,row=0, style=discord.ButtonStyle.green)
    async def myBtn1(self,interaction: discord.Interaction,button: discord.ui.Button):

        if((self.votingTurn%2==0 and self.cap1 == interaction.user.id) or (self.votingTurn%2==1 and self.cap2 == interaction.user.id)):
            button.disabled = True  # disabling the button
            self.votingTurn+=1
            self.mapleft-=1
            if (self.mapleft != 0):
                await interaction.response.edit_message(
                    view=self)  # updating the view of message (as we bisabled the button)
            else:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title="Map Selected",
                    description="**Breeze**")
                embed.add_field(name="Map Type", value="Spike Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                embed.set_footer(text="Powered by Valorant")
                embed.set_image(url="https://cdn.esportsdriven.com/media/upload/images/Breeze_For_Kayo.large.jpg")
                await interaction.response.send_message(embed=embed, view=None)


    @discord.ui.button(label="Bind" ,row=0, style=discord.ButtonStyle.green)
    async def myBtn2(self,interaction: discord.Interaction,button: discord.ui.Button):

        if((self.votingTurn%2==0 and self.cap1 == interaction.user.id) or (self.votingTurn%2==1 and self.cap2 == interaction.user.id)):
            button.disabled = True  # disabling the button
            self.votingTurn += 1
            self.mapleft -= 1
            if (self.mapleft != 0):
                await interaction.response.edit_message(
                    view=self)  # updating the view of message (as we bisabled the button)
            else:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title="Map Selected",
                    description="**Bind**")
                embed.add_field(name="Map Type", value="Spike Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                embed.set_footer(text="Powered by Valorant")
                embed.set_image(url="https://preview.redd.it/jts58xw03sb61.png?width=1366&format=png&auto=webp&v=enabled&s=f68717289a7a1470319f7b70a80966835149367b")
                await interaction.response.send_message(embed=embed, view=None)


    @discord.ui.button(label="Split" ,row=0, style=discord.ButtonStyle.green)
    async def myBtn3(self,interaction: discord.Interaction,button: discord.ui.Button):

        if((self.votingTurn%2==0 and self.cap1 == interaction.user.id) or (self.votingTurn%2==1 and self.cap2 == interaction.user.id)):
            button.disabled = True  # disabling the button
            self.votingTurn += 1
            self.mapleft -= 1
            if (self.mapleft != 0):
                await interaction.response.edit_message(
                    view=self)  # updating the view of message (as we bisabled the button)
            else:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title="Map Selected",
                    description="**Split**")
                embed.add_field(name="Map Type", value="Spike Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                embed.set_footer(text="Powered by Valorant")
                embed.set_image(url="https://whatifgaming.com/wp-content/uploads/2023/01/Split-Loading-Screen-1536x863.png.webp")
                await interaction.response.send_message(embed=embed, view=None)



    @discord.ui.button(label="Haven" ,row=0, style=discord.ButtonStyle.green)
    async def myBtn4(self,interaction: discord.Interaction,button: discord.ui.Button):

        if((self.votingTurn%2==0 and self.cap1 == interaction.user.id) or (self.votingTurn%2==1 and self.cap2 == interaction.user.id)):
            button.disabled = True  # disabling the button
            self.votingTurn += 1
            self.mapleft -= 1
            if (self.mapleft != 0):
                await interaction.response.edit_message(
                    view=self)  # updating the view of message (as we bisabled the button)
            else:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title="Map Selected",
                    description="**Haven**")
                embed.add_field(name="Map Type", value="Spike Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                embed.set_footer(text="Powered by Valorant")
                embed.set_image(url="https://static0.gamerantimages.com/wordpress/wp-content/uploads/2022/10/Featured---Valorant-Guide-to-the-Haven-Map.jpg?q=50&fit=contain&w=1140&h=&dpr=1.5")
                await interaction.response.send_message(embed=embed, view=None)

    @discord.ui.button(label="Ascent",row=0, style=discord.ButtonStyle.green)
    async def myBtn5(self, interaction: discord.Interaction, button: discord.ui.Button):

        if ((self.votingTurn % 2 == 0 and self.cap1 == interaction.user.id) or (
                self.votingTurn % 2 == 1 and self.cap2 == interaction.user.id)):
            button.disabled = True  # disabling the button
            self.votingTurn += 1
            self.mapleft -= 1
            if (self.mapleft != 0):
                await interaction.response.edit_message(
                    view=self)  # updating the view of message (as we bisabled the button)
            else:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title="Map Selected",
                    description="**Ascent**")
                embed.add_field(name="Map Type", value="Spike Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                embed.set_footer(text="Powered by Valorant")
                embed.set_image(url="https://win.gg/wp-content/uploads/2022/05/ascent-loading-screen.jpg")
                await interaction.response.send_message(embed=embed, view=None)

    @discord.ui.button(label="Icebox",row=1, style=discord.ButtonStyle.green)
    async def myBtn6(self, interaction: discord.Interaction, button: discord.ui.Button):

        if ((self.votingTurn % 2 == 0 and self.cap1 == interaction.user.id) or (
                self.votingTurn % 2 == 1 and self.cap2 == interaction.user.id)):
            button.disabled = True  # disabling the button
            self.votingTurn += 1
            self.mapleft -= 1
            if (self.mapleft != 0):
                await interaction.response.edit_message(
                    view=self)  # updating the view of message (as we bisabled the button)
            else:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title="Map Selected",
                    description="**Icebox**")
                embed.add_field(name="Map Type", value="Spike Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                embed.set_footer(text="Powered by Valorant")
                embed.set_image(url="https://img.redbull.com/images/q_auto,f_auto/redbullcom/2020/11/4/lwvjgoxionoqelsmdd3z/valorant-ice-box-overview")
                await interaction.response.send_message(embed=embed, view=None)

    @discord.ui.button(label="Fracture",row=1, style=discord.ButtonStyle.green)
    async def myBtn7(self, interaction: discord.Interaction, button: discord.ui.Button):

        if ((self.votingTurn % 2 == 0 and self.cap1 == interaction.user.id) or (
                self.votingTurn % 2 == 1 and self.cap2 == interaction.user.id)):
            button.disabled = True  # disabling the button
            self.votingTurn += 1
            self.mapleft -= 1
            if (self.mapleft != 0):
                await interaction.response.edit_message(
                    view=self)  # updating the view of message (as we bisabled the button)
            else:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title="Map Selected",
                    description="**Fracture**")
                embed.add_field(name="Map Type", value="Spike Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                embed.set_footer(text="Powered by Valorant")
                embed.set_image(url="https://www.valorantpcdownload.com/wp-content/uploads/2021/09/FMain-4-1536x893.png")
                await interaction.response.send_message(embed=embed, view=None)



class Valo(commands.Cog):

    def __int__(self,bot):
        self.bot = bot

    @commands.command(name="valo")
    async def valo(self,ctx,cap1: discord.Member,cap2: discord.Member):

        #print(cap1.id)

        await ctx.send("Captains Ban Maps Below", view=ValoVeto(cap1.id, cap2.id)) #call mybutton calss with sending captian ids
        print("bumton")








async def setup(bot):
    await bot.add_cog(Valo(bot))