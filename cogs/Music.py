import discord
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch
from pytube import YouTube

Global_play = {}
Global_Pause = {}
Global_Queue = {}

VoiceClient = {}

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
        super().__init__(timeout=None)

    @discord.ui.button(label="Pause" ,emoji = "⏸",row=0, style=discord.ButtonStyle.green)
    async def pauseBut(self,interaction: discord.Interaction,button: discord.ui.Button):
        print("paused")
        self.vc.pause()
        global Global_Pause
        Global_Pause[self.ctx.guild.id] = True
        global Global_play
        Global_play[self.ctx.guild.id] = False
        await interaction.response.defer()
    @discord.ui.button(label="Play" ,emoji = "▶",row=0, style=discord.ButtonStyle.green)
    async def playBut(self,interaction: discord.Interaction,button: discord.ui.Button):
        self.vc.resume()
        global Global_play
        Global_play[self.ctx.guild.id] = True
        global Global_Pause
        Global_Pause[self.ctx.guild.id] = False
        await interaction.response.defer()
    @discord.ui.button(label="Skip" ,emoji = "⏭",row=0, style=discord.ButtonStyle.green)
    async def skipBut(self,interaction: discord.Interaction,button: discord.ui.Button):
        await self.ctx.send("!s",delete_after = 0.1)
        await interaction.response.edit_message(view = None)
        await interaction.response.defer()
    @discord.ui.button(label="Clear" ,emoji = "🗑️",row=1, style=discord.ButtonStyle.green)
    async def clearBut(self,interaction: discord.Interaction,button: discord.ui.Button):
        # await self.ctx.send("!leave",delete_after = 0.1)
        await interaction.response.defer()
        global Global_play,Global_Pause,Global_Queue
        Global_Pause[self.ctx.guild.id] = False
        Global_play[self.ctx.guild.id] = False
        Global_Queue[self.ctx.guild.id]  = []
        await self.vc.stop()
        await interaction.response.edit_message(view = None)
        await self.ctx.send("Queue Emptied")
        
    @discord.ui.button(label="Leave" ,emoji = "❌",row=1, style=discord.ButtonStyle.green)
    async def leaveBut(self,interaction: discord.Interaction,button: discord.ui.Button):
        # await self.ctx.send("!leave",delete_after = 0.1)
        global Global_play,Global_Pause,Global_Queue
        Global_Pause[self.ctx.guild.id] = False
        Global_play[self.ctx.guild.id] = False
        del Global_Queue[self.ctx.guild.id] 
        await self.vc.disconnect()
        await interaction.response.edit_message(view = None)
        await interaction.response.defer()
        
class Music(commands.Cog):
    def __init__(self,bot):
        
        #basic variables and objects -- self explanatory
        self.bot = bot
        self.Playing = {}
        self.Paused = {}
        self.if_skipped = {}
        self.Queue = {}
        self.vc = {}
        self.YDL_sett = {'format':'bestaudio','noplaylist':'True'}
        self.FFMPEG_sett = {'options': '-vn -b:a 320k','executable': r"./assets/ffmpeg/bin/ffmpeg.exe" , 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
# 'executable': r"./assets/ffmpeg/bin/ffmpeg.exe",

    
    

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
    
    def new_search_yt(self,text):
        if "https://www.youtube.com/" in text:
            url = text
        else:
            print("working")
            result = VideosSearch (text, limit=1).result()['result']
            # print(result)
            url = result[0]['link']
            # title = result['title']
            # thumbnail = result["thumbnails"]["url"]
        # print(url)
        yt = YouTube(url)
        
        source_url = yt.streaming_data['formats'][0]['url']    
        title = result[0]['title']
        thumbnail = result[0]['thumbnails'][0]['url']
        # try:
        #     thumbnail = result[0]['richThumbnail']['url']
        # except:
        #     thumbnail = result[0]['thumbnails'][0]['url']
        # print(source_url)
        return {'source' : source_url , 'title' : title , 'thumbnail' : thumbnail}


    def my_after(self,ctx):
        fut = asyncio.run_coroutine_threadsafe(self.nowPlaying(ctx),self.bot.loop)
        try:
            fut.result()
            return
        except:
            pass


    async def play_music(self, ctx):
        global Global_play,Global_Queue
        global Global_Pause
        self.Queue = Global_Queue
        self.Playing[ctx.guild.id] = Global_play[ctx.guild.id]
        self.Paused[ctx.guild.id] = Global_Pause[ctx.guild.id]
        # print(len(self.Queue[ctx.guild.id]))
        # print(self.Queue[ctx.guild.id])
        # print(self.Queue[ctx.guild.id][0]['source'])
        if len(self.Queue[ctx.guild.id]) > 0:
            self.Playing[ctx.guild.id] = True
            Global_play[ctx.guild.id] = True
            m_url = self.Queue[ctx.guild.id][0][0]['source']
        
            if self.vc[ctx.guild.id] == None or not self.vc[ctx.guild.id].is_connected():
                self.vc[ctx.guild.id] = await self.Queue[ctx.guild.id][0][1].connect()
                
                if self.vc[ctx.guild.id] == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            
            try:
                print("0")
                self.vc[ctx.guild.id].play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_sett), after=lambda e: self.play_next(ctx))
                print("1")
                await self.nowPlaying(ctx)
                
            except Exception as error:
                print(error)
        
        else :
            self.Playing[ctx.guild.id] = False
            # global Global_play
            Global_play[ctx.guild.id] = False
    
    @commands.Cog.listener()
    async def on_message(self,message):
        
        if message.content == "!s" and message.author.id == BOT_ID:
            #print(f"Works and {message.author.id}")
            ctx = await self.bot.get_context(message)
            await self.skip(ctx)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        for i in VoiceClient:
            id = i
            if len(self.bot.get_guild(id).voice_client.channel.members) == 1:
                await asyncio.sleep(20)
                if len(self.bot.get_guild(id).voice_client.channel.members) == 1:
                    await self.bot.get_guild(id).voice_client.disconnect()
                    del VoiceClient[id]
    
    def play_next (self,ctx):
        
        global Global_play,Global_Queue
        self.Playing[ctx.guild.id] = Global_play[ctx.guild.id]
        self.Paused[ctx.guild.id] = Global_Pause[ctx.guild.id]
        self.Queue = Global_Queue

        # The first playing song is removed from the queue and the second song is now at 0th index
        if not self.if_skipped[ctx.guild.id]:
            self.Queue[ctx.guild.id].pop(0)
        self.if_skipped[ctx.guild.id] = False
        
        if len(self.Queue[ctx.guild.id]) > 0:
            self.Playing[ctx.guild.id] = True
            Global_play[ctx.guild.id] = True
            
            m_url = self.Queue[ctx.guild.id][0][0]['source']
            self.vc[ctx.guild.id].play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_sett), after=lambda e: self.play_next(ctx))
            try:
                self.my_after(ctx)
            except:
                print("ye nhi chalrha")
        else:
            self.Playing[ctx.guild.id] = False
            # global Global_play
            Global_play[ctx.guild.id] = False

    @commands.command (name = "play" ,aliases=["p", "playing"], help="Play the selected song from youtube")
    async def play (self, ctx, *args):
        global Global_play
        global Global_Pause
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            if ctx.author.voice and ctx.author.voice.channel:
                self.vc[ctx.guild.id] = await voice_channel.connect()
                self.Playing[ctx.guild.id] = False
                self.Paused[ctx.guild.id] = False
                self.if_skipped[ctx.guild.id] = False

                Global_play[ctx.guild.id] = False
                Global_Pause[ctx.guild.id] = False
                print(self.Playing)
                print(self.Paused)
                print(self.Paused)

        print("t1")
        # global Global_Pause
        # global Global_play
        global VoiceClient
        VoiceClient[ctx.guild.id] = ctx.author.voice.channel
        self.Queue = Global_Queue
        print("t2")
        self.Playing[ctx.guild.id] = Global_play[ctx.guild.id]
        self.Paused[ctx.guild.id] = Global_Pause[ctx.guild.id]
        print("t3")
        
        query =" ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        elif self.Paused[ctx.guild.id] and query == "":
            self.vc[ctx.guild.id].resume ()
            self.Paused[ctx.guild.id] = False
            self.Playing[ctx.guild.id] = True
            Global_Pause[ctx.guild.id] = False
            Global_play[ctx.guild.id] = True
        else:
            song = self.new_search_yt(query)
            if type (song) == type (True):
                await ctx.send("Could not download the song. Incorrect format, try a different keyword")
            else:
                await ctx.send(f"Song added to the queue -- ```{song['title']}```")
                print("faux1")
                try:
                    self.Queue[ctx.guild.id].append([song, voice_channel])
                except:
                    self.Queue[ctx.guild.id] = [[song, voice_channel]]
               #self.Queue[ctx.guild.id].append([song, voice_channel])
                for data in self.Queue[ctx.guild.id]:
                    print("Data : ",end="")
                    print(data)
                print("faux2")
                print("faux3")
                if self.Playing[ctx.guild.id] == False and self.Paused[ctx.guild.id] == False:
                    print("faux4")
                    await self.play_music(ctx)
                    print("faux5")

        

    async def nowPlaying(self,ctx):
        #await ctx.send("```Now Playing---```")
        url = self.Queue[ctx.guild.id][0][0]['thumbnail']
        try :
            embed = discord.Embed(
                colour = discord.Colour.green(),
                title = "Now Playing"
                ) 
            embed.add_field(name  = f"{self.Queue[ctx.guild.id][0][0]['title']}" , value = "")
            embed.set_image(url=url)
        except:
            print("hagdiya")
        #await ctx.send(self.Queue[0][0]['title'])
        await ctx.send(embed = embed,view = Pause(self.vc[ctx.guild.id],ctx,self.Playing[ctx.guild.id],self.Paused[ctx.guild.id]))


    @commands.command(name = "pause" ,aliases = ["paused",] ,help = "")
    async def pause(self,ctx,*args):
        global Global_Pause
        global Global_play
        self.Playing[ctx.guild.id] = Global_play[ctx.guild.id]
        self.Paused[ctx.guild.id] = Global_Pause[ctx.guild.id]
        
        # Pauses the song if playing AND resumes the song if paused
        voice_channel = ctx.author.voice.channel
        
        if voice_channel is None or not self.vc[ctx.guild.id].is_connected():
            await ctx.send("Connect to a voice channel!")
        elif self.Playing[ctx.guild.id]:
            self.vc[ctx.guild.id].pause()
            self.Paused[ctx.guild.id] = True
            self.Playing[ctx.guild.id] = False
            Global_Pause[ctx.guild.id] = True
            Global_play[ctx.guild.id] = False
            await ctx.send("Paused.")
        elif self.Paused[ctx.guild.id]:
            self.vc[ctx.guild.id].resume()
            self.Paused[ctx.guild.id] = False
            self.Playing[ctx.guild.id] = True
            Global_Pause[ctx.guild.id] = False
            Global_play[ctx.guild.id] = True
            await ctx.send("Playing now.")
        else:
            await ctx.send("Could not pause!")
    
    @commands.command(name="resume",aliases = ["r",],help = "")
    async def resume(self,ctx,*args):
        global Global_Pause
        global Global_play
        self.Playing[ctx.guild.id] = Global_play[ctx.guild.id]
        self.Paused[ctx.guild.id] = Global_Pause[ctx.guild.id]
        
        #Resumes the song if paused
        
        if self.Paused[ctx.guild.id]:
            self.Paused[ctx.guild.id] = False
            self.Playing[ctx.guild.id] = True
            
            Global_Pause[ctx.guild.id] = False
            Global_play[ctx.guild.id] = True
            self.vc[ctx.guild.id].resume()

    @commands.command (name="skip", aliases=["s"], help = "Skips the currently played song")
    async def skip(self, ctx, *args):
        global Global_Pause,Global_Queue
        global Global_play
        self.Queue = Global_Queue
        self.Playing[ctx.guild.id] = Global_play[ctx.guild.id]
        self.Paused[ctx.guild.id] = Global_Pause[ctx.guild.id]
        
        #Skips the current playing song and pops it form the queue
        
        if self.vc[ctx.guild.id] != None:
            if self.Playing[ctx.guild.id]:
                self.vc[ctx.guild.id].stop()
            self.if_skipped[ctx.guild.id] = True
            
            await ctx.send(f"Skipped ```{self.Queue[ctx.guild.id].pop(0)[0]['title']}```")
            self.Playing[ctx.guild.id] = False
            self.Paused[ctx.guild.id] = False
            Global_Pause[ctx.guild.id] = False
            Global_play[ctx.guild.id] = False
            await self.play_music(ctx)
        
    @commands.command(name="join",help="")
    async def join(self,ctx,*args):
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            if ctx.author.voice and ctx.author.voice.channel:
                self.vc[ctx.guild.id] = await voice_channel.connect()
                self.Playing[ctx.guild.id] = False
                self.Paused[ctx.guild.id] = False
                self.if_skipped[ctx.guild.id] = False

                global Global_play
                global Global_Pause
                Global_play[ctx.guild.id] = False
                Global_Pause[ctx.guild.id] = False
                global VoiceClient
                VoiceClient[ctx.guild.id] = ctx.author.voice.channel
                print(self.Playing)
                print(self.Paused)
                print(self.Paused)

        # voice_channel = ctx.author.voice.channel
        # if self.vc == None or not self.vc.is_connected():
        #     self.vc = await voice_channel.connect()
            
    @commands.command (name="queue", aliases=["q"], help="Displays all the songs currently in the queue")
    async def queue (self, ctx):
        global Global_Queue
        #Prints the Queue of the songs-- upto 10 songs 
        self.Queue = Global_Queue
        retval = ""
        
        for i in range(0, len(self.Queue[ctx.guild.id])):
            if i > 10: break
            if i == 0:
                retval += "1." + self.Queue[ctx.guild.id][i][0]['title'] + '(Playing Now)' + '\n'
            else:
                retval += f"{i+1}." + self.Queue[ctx.guild.id][i][0]['title'] + '\n'
        if retval != "":
            retval = "```\n" +retval+ "```"
            await ctx.send(retval)
        else:
            await ctx.send("No music in the queue.")
    

    @commands.command (name="empty", aliases=["c", "bin"], help="Stops the current song and clears the queue")
    async def empty(self, ctx, *args):
        
        # Clear command empties the Queue and stops the current playing track.
        # Essentially it stops all music playing or to be played
        print("empty")
        
        if self.vc[ctx.guild.id] != None and self.Playing[ctx.guild.id]:
            self.vc[ctx.guild.id].stop()
            self.Queue[ctx.guild.id] = []
            await ctx.send("Music queue cleared")
            self.Playing[ctx.guild.id] = False
            self.Paused[ctx.guild.id] = False
            global Global_Pause
            Global_Pause[ctx.guild.id] = False
            global Global_play
            Global_play[ctx.guild.id] = False

    
    @commands.command (name = "leave", help = "Removes the bot from the voice channel")
    async def leave(self,ctx):
        
        #Simply checks if the bot is connected to a VC and if True disconnects it from the channel 
        await self.vc[ctx.guild.id].disconnect()
        self.Playing[ctx.guild.id] = False
        self.Paused[ctx.guild.id] = False
        global Global_Pause
        Global_Pause[ctx.guild.id] = False
        global Global_play
        Global_play[ctx.guild.id] = False
        self.Queue[ctx.guild.id] = []

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