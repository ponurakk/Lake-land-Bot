import discord
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord.utils import get
from discord.ext import commands

class Bcolors:
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Grey = '\033[90m'
    Black = '\033[90m'
    Default = '\033[99m'
    Bold = '\033[1m'
    Italic = '\033[3m'
    Underline = '\033[4m'
    ENDC = '\033[0m'
players = {}
class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Bcolors.Green}{self.__class__.__name__}{Bcolors.ENDC} Cog has been loaded\n-----")
    
    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
    
    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            voice = await channel.disconnect()
        else:
            voice = await channel.disconnect()



    # command to play sound from a youtube URL
    @commands.command()
    async def play(self, ctx, url):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            await ctx.send('Muzyka powinna grać, jeśli nie spróbuj mnie wyrzucić i jeszcze raz dołączyć.')

    # check if the bot is already playing
        else:
            await ctx.send("Już gram jedną piosenkę.")
            return


    # command to resume voice if it is paused
    @commands.command()
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            voice.resume()
            await ctx.send('Wznawiam...')


    # command to pause voice if it is playing
    @commands.command()
    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
            await ctx.send('Piosenka została spauzowana')


    # command to stop voice
    @commands.command()
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            await ctx.send('Zatrzymuję...')

def setup(client):
    client.add_cog(Music(client))
