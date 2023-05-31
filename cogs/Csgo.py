import discord
from discord.ui import Button,View
from discord.ext import commands

class CsgoVeto(discord.ui.View):
    #This is a button view class which is called later ine code

    def __init__(self,cap1,cap2):
        super().__init__()
        ##~~~~~~~~~~~~~DECLARE ALL VARIABLES HERE USING self.varName = varValue ~~~~~~~~~~~~~~~~~~~~~~~~~~##
        self.value=None
        self.cap1 = cap1
        self.cap2 = cap2
        self.mapleft = 7
        self.votingTurn=0 #odd means cap1 and even means cap2
        #self.mapList = ["Miraj","Dust 2","Inferno"]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Veto Buttons~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @discord.ui.button(label="Mirage" , style=discord.ButtonStyle.green, emoji="<:mirage:1108662742409293854>")
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
                    description="**Mirage**"
                )
                # Add more detailed information about the map
                embed.add_field(name="Map Type", value="Bomb Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                # Set a footer with additional information
                embed.set_footer(text="CS:GO - Counter-Strike: Global Offensive")

                # Set a larger image within the embed
                embed.set_image(url="https://static.wikia.nocookie.net/cswikia/images/1/1e/CSGO_Mirage_latest_version.jpg/revision/latest?cb=20200301201524")
                await interaction.response.send_message(embed=embed, view=None)


    @discord.ui.button(label="Dust 2" , style=discord.ButtonStyle.green,emoji="<:d2:1108662260244676679>")
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
                    description="**Dust 2**"
                )
                # Add more detailed information about the map
                embed.add_field(name="Map Type", value="Bomb Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                # Set a footer with additional information
                embed.set_footer(text="CS:GO - Counter-Strike: Global Offensive")

                # Set a larger image within the embed
                embed.set_image(url="https://img.redbull.com/images/c_crop,x_0,y_48,h_768,w_1920/c_fill,w_1680,h_700/q_auto,f_auto/redbullcom/2020/7/15/mdlhtjaz85gjhahyakce/csgo-dust-2-map")
                await interaction.response.send_message(embed=embed, view=None)


    @discord.ui.button(label="Inferno" , style=discord.ButtonStyle.green,emoji="<:inferno:1108662264254435369>")
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
                    description="**Inferno**"
                )
                # Add more detailed information about the map
                embed.add_field(name="Map Type", value="Bomb Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                # Set a footer with additional information
                embed.set_footer(text="CS:GO - Counter-Strike: Global Offensive")

                # Set a larger image within the embed
                embed.set_image(url="https://static.wikia.nocookie.net/cswikia/images/0/0d/De_inferno_cs2.png/revision/latest/scale-to-width-down/1000?cb=20230325174530")
                await interaction.response.send_message(embed=embed, view=None)



    @discord.ui.button(label="Nuke" , style=discord.ButtonStyle.green,emoji="<:nuke:1108662268591341588>")
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
                    description="**Nuke**"
                )
                # Add more detailed information about the map
                embed.add_field(name="Map Type", value="Bomb Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                # Set a footer with additional information
                embed.set_footer(text="CS:GO - Counter-Strike: Global Offensive")

                # Set a larger image within the embed
                embed.set_image(url="https://estnn.com/wp-content/uploads/2022/03/CSGO_Nuke_22_Nov_2019_update_picture_1-747x420.webp")
                await interaction.response.send_message(embed=embed, view=None)

    @discord.ui.button(label="Overpass",row=0, style=discord.ButtonStyle.green,emoji="<:overpass:1108662274358530069>")
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
                    description="**Overpass**"
                )
                # Add more detailed information about the map
                embed.add_field(name="Map Type", value="Bomb Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                # Set a footer with additional information
                embed.set_footer(text="CS:GO - Counter-Strike: Global Offensive")

                # Set a larger image within the embed
                embed.set_image(url="https://static.wikia.nocookie.net/cswikia/images/5/55/Overpass_loading_screen.png/revision/latest?cb=20230401221615")
                await interaction.response.send_message(embed=embed, view=None)

    @discord.ui.button(label="Vertigo",row=1, style=discord.ButtonStyle.green,emoji="<:vertigo:1108662279181979659>")
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
                    description="**Vertigo**"
                )
                # Add more detailed information about the map
                embed.add_field(name="Map Type", value="Bomb Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                # Set a footer with additional information
                embed.set_footer(text="CS:GO - Counter-Strike: Global Offensive")

                # Set a larger image within the embed
                embed.set_image(url="https://static.wikia.nocookie.net/cswikia/images/8/88/De_vertigo_cs2.jpg/revision/latest/scale-to-width-down/1000?cb=20230324175743")
                await interaction.response.send_message(embed=embed, view=None)

    @discord.ui.button(label="Anubis",row=1, style=discord.ButtonStyle.green,emoji="<:anubis:1108662254007758959>")
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
                    description="**Anubis**"
                )
                # Add more detailed information about the map
                embed.add_field(name="Map Type", value="Bomb Defusal", inline=True)
                embed.add_field(name="Max Players", value="10", inline=True)
                # Set a footer with additional information
                embed.set_footer(text="CS:GO - Counter-Strike: Global Offensive")

                # Set a larger image within the embed
                embed.set_image(url="https://static.wikia.nocookie.net/cswikia/images/5/54/De_anubis.png/revision/latest?cb=20200401081330")
                await interaction.response.send_message(embed=embed, view=None)





    # @discord.ui.button(label="Captain 2", style=discord.ButtonStyle.green)
    # async def myBtn5(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     cap2 = interaction.user.id
    #     button.disabled = True
    #     await interaction.response.edit_message(view=self)
    #     print(cap2)




class Csgo(commands.Cog):

    def __int__(self,bot):
        self.bot = bot



    @commands.command(name="csgo")
    async def csgo(self,ctx,cap1: discord.Member,cap2: discord.Member):

        await ctx.send("Captains Ban Maps Below", view=CsgoVeto(cap1.id,cap2.id)) #call mybutton calss with sending captian ids


async def setup(bot):
    await bot.add_cog(Csgo(bot))








