import discord
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

Global_play = False
Global_Pause = False



###########################################
BOT_ID = 1095747361164230826 
###########################################

#Imported Required modules for code and created music class for writing the Music cog
class Pause(discord.ui.View):
    def __init__(self,vc,ctx,play,pause):
        self.vc = vc
        self.ctx = ctx
        self.Playing = play
        self.Paused = pause
        super().__init__()
    
    @discord.ui.button(label="Pause" ,emoji = "⏸",row=0, style=discord.ButtonStyle.green)
    async def pauseBut(self,interaction: discord.Interaction,button: discord.ui.Button):
        self.vc.pause()
        global Global_Pause
        Global_Pause = True
        global Global_play
        Global_play = False
        
        await interaction.response.defer()
    @discord.ui.button(label="Play" ,emoji = "▶",row=0, style=discord.ButtonStyle.green)
    async def playBut(self,interaction: discord.Interaction,button: discord.ui.Button):
        self.vc.resume()
        global Global_play
        Global_play = True
        global Global_Pause
        Global_Pause = False
        await interaction.response.defer()
    @discord.ui.button(label="Skip" ,emoji = "⏭",row=0, style=discord.ButtonStyle.green)
    async def skipBut(self,interaction: discord.Interaction,button: discord.ui.Button):
        await self.ctx.send("!s",delete_after = 0.1)
        await interaction.response.edit_message(view = None)
        await interaction.response.defer()
        
class Music(commands.Cog):
    def __init__(self,bot):
        
        #basic variables and objects -- self explanatory
        self.bot = bot
        self.Playing = False
        self.Paused = False
        self.if_skipped = False
        self.Queue = []
        self.YDL_sett = {'format':'bestaudio','noplaylist':'True'}
        self.FFMPEG_sett = {'options': '-vn -b:a 320k', 'executable': r"./assets/ffmpeg/bin/ffmpeg.exe", 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}

        self.vc = None
    
    

    def search_yt(self,text):
        
        # This function takes in the query and extracts a audio link of the song from youtube using YouTube_DL
        # We do not download the video/audio and stream it directly
        # It returns a dictionary containg the url(under source key) and name of the song(under title key) 
        
        with YoutubeDL(self.YDL_sett) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{text}",download=False)['entries'][0]
            except Exception :
                return False
        
        return {'source' : info['formats'][0]['url'],'title':info['title'],'thumbnail':info['thumbnails'][0]['url']}
    
    def my_after(self,ctx):
        fut = asyncio.run_coroutine_threadsafe(self.nowPlaying(ctx),self.bot.loop)
        try:
            fut.result()
            return
        except:
            pass


    async def play_music(self, ctx):
        global Global_play
        self.Playing = Global_play
        self.Paused = Global_Pause
        
        if len(self.Queue) > 0:
            self.Playing = True
            
            Global_play = True
            m_url = self.Queue[0][0]['source']
            
        
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.Queue[0][1].connect()
                
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            
            try:
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_sett), after=lambda e: self.play_next(ctx))
                await self.nowPlaying(ctx)
                
            except:
                print("some error occured !")
        
        else :
            self.Playing = False
            # global Global_play
            Global_play = False
    
    @commands.Cog.listener()
    async def on_message(self,message):
        
        if message.content == "!s" and message.author.id == BOT_ID:
            #print(f"Works and {message.author.id}")
            ctx = await self.bot.get_context(message)
            await self.skip(ctx)

    def play_next (self,ctx):
        
        
        global Global_play
        self.Playing = Global_play
        self.Paused = Global_Pause
        
        # The first playing song is removed from the queue and the second song is now at 0th index
        if not self.if_skipped:
            self.Queue.pop(0)
        self.if_skipped = False
        
        if len(self.Queue) > 0:
            self.Playing = True
            Global_play = True
            
            m_url = self.Queue[0][0]['source']
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_sett), after=lambda e: self.play_next(ctx))
            try:
                self.my_after(ctx)
            except:
                print("ye nhi chalrha")
        else:
            self.Playing = False
            # global Global_play
            Global_play = False

    @commands.command (name = "play" ,aliases=["p", "playing"], help="Play the selected song from youtube")
    async def play (self, ctx, *args):
        global Global_Pause
        global Global_play
        self.Playing = Global_play
        self.Paused = Global_Pause
        
        query =" ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        elif self.Paused and query == "":
            self.vc.resume ()
            self.Paused = False
            self.Playing = True

            Global_Pause = False
            Global_play = True
        else:
            song = self.search_yt (query)
            if type (song) == type (True):
                await ctx.send("Could not download the song. Incorrect format, try a different keyword")
            else:
                await ctx.send(f"Song added to the queue -- ```{song['title']}```")

                self.Queue.append([song, voice_channel])
                if self.Playing == False and self.Paused == False:
                    await self.play_music(ctx)

        

    async def nowPlaying(self,ctx):
        #await ctx.send("```Now Playing---```")
        url = self.Queue[0][0]['thumbnail']
        try :
            embed = discord.Embed(
                colour = discord.Colour.green(),
                title = "Now Playing"
                ) 
            embed.add_field(name  = f"{self.Queue[0][0]['title']}" , value = "")
            embed.set_image(url=url)
        except:
            print("hagdiya")
        #await ctx.send(self.Queue[0][0]['title'])
        await ctx.send(embed = embed,view = Pause(self.vc,ctx,self.Playing,self.Paused))
        

    @commands.command(name = "pause" ,aliases = ["paused",] ,help = "")
    async def pause(self,ctx,*args):
        global Global_Pause
        global Global_play
        self.Playing = Global_play
        self.Paused = Global_Pause
        
        # Pauses the song if playing AND resumes the song if paused
        voice_channel = ctx.author.voice.channel
        
        if voice_channel is None or not self.vc.is_connected():
            await ctx.send("Connect to a voice channel!")
        elif self.Playing:
            self.vc.pause()
            self.Paused = True
            self.Playing = False
            Global_Pause = True
            Global_play = False
            await ctx.send("Paused.")
        elif self.Paused:
            self.vc.resume()
            self.Paused = False
            self.Playing = True
            Global_Pause = False
            Global_play = True
            await ctx.send("Playing now.")
        else:
            await ctx.send("Could not pause!")
    
    @commands.command(name="resume",aliases = ["r",],help = "")
    async def resume(self,ctx,*args):
        global Global_Pause
        global Global_play
        self.Playing = Global_play
        self.Paused = Global_Pause
        
        #Resumes the song if paused
        
        if self.Paused:
            self.Paused = False
            self.Playing = True
            
            Global_Pause = False
            Global_play = True
            self.vc.resume()

    @commands.command (name="skip", aliases=["s"], help = "Skips the currently played song")
    async def skip(self, ctx, *args):
        global Global_Pause
        global Global_play
        
        self.Playing = Global_play
        self.Paused = Global_Pause
        
        #Skips the current playing song and pops it form the queue
        
        if self.vc != None:
            if self.Playing:
                self.vc.stop()
            self.if_skipped = True
            
            await ctx.send(f"Skipped ```{self.Queue.pop(0)[0]['title']}```")
            self.Playing = False
            self.Paused = False
            Global_Pause = False
            Global_play = False
            await self.play_music(ctx)
        
    @commands.command(name="join",help="")
    async def join(self,ctx,*args):
        voice_channel = ctx.author.voice.channel
        if self.vc == None or not self.vc.is_connected():
            self.vc = await voice_channel.connect()
            
    @commands.command (name="queue", aliases=["q"], help="Displays all the songs currently in the queue")
    async def queue (self, ctx):
        
        #Prints the Queue of the songs-- upto 10 songs 
        
        retval = ""
        
        for i in range(0, len(self.Queue)):
            if i > 10: break
            if i == 0:
                retval += "1." + self.Queue[i][0]['title'] + '(Playing Now)' + '\n'
            else:
                retval += f"{i+1}." + self.Queue[i][0]['title'] + '\n'
        if retval != "":
            retval = "```\n" +retval+ "```"
            await ctx.send(retval)
        else:
            await ctx.send("No music in the queue.")
    

    @commands.command (name="empty", aliases=["c", "bin"], help="Stops the current song and clears the queue")
    async def empty(self, ctx, *args):
        
        # Clear command empties the Queue and stops the current playing track.
        # Essentially it stops all music playing or to be played
        
        if self.vc != None and self.Playing:
            self.vc.stop()
            self.Queue = []
            await ctx.send("Music queue cleared")

    
    @commands.command (name = "leave", help = "Removes the bot from the voice channel")
    async def leave(self,ctx):
        
        #Simply checks if the bot is connected to a VC and if True disconnects it from the channel 
        await self.vc.disconnect()
        self.Playing = False
        self.Paused = False
        global Global_Pause
        Global_Pause = False
        global Global_play
        Global_play = False
        self.Queue = []

    @commands.Cog.listener()
    async def on_ready(self):
        await print("Music Ready")
    
    @commands.command()
    async def echo(self,ctx):
        data = ctx.message.content
        await ctx.send(data)

#Finally this is function helps connect the cog to main.py

async def setup(bot):
    await bot.add_cog(Music(bot))