import discord
import asyncio
import random
import datetime
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

class Admin_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Bcolors.Green}Admin_Commands{Bcolors.ENDC} loaded')
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, duration: int, time_type: str, *, prize: str):
        ldigit = duration%10
        if time_type == 's':
            time_name = 'sekundy'
        elif time_type == 'm':
            time_name = 'minuty'
        elif time_type == 'g':
            time_name = 'godziny'
        elif time_type == 'd':
            time_name = 'dni'
        
        embed = discord.Embed(title=prize,
                            description=f"Hostowany przez: {ctx.author.mention}\nZareaguj :tada: by dołączyć!\nPozostały czas: **{duration}** {time_name}",
                            colour=discord.Colour.from_rgb(135, 255, 16),
                            timestamp=datetime.datetime.utcnow())
        time_start = datetime.datetime.utcnow()

        msg = await ctx.channel.send(content=":tada: **GIVEAWAY** :tada:", embed=embed)
        await msg.add_reaction("🎉")
        if time_type == 's':
            duration = duration
        elif time_type == 'm':
            duration = duration*60
        elif time_type == 'g':
            duration = duration*3600
        elif time_type == 'd':
            duration = duration*86400
        await asyncio.sleep(duration)
        new_msg = await ctx.channel.fetch_message(msg.id)

        user_list = [u for u in await new_msg.reactions[0].users().flatten() if u != self.client.user] # Check the reactions/don't count the bot reaction

        if len(user_list) == 0:
            await ctx.send("Nikt nie zareagował. :7000squidpepe:") 
        else:
            winner = random.choice(user_list)
            e = discord.Embed(title=f"{prize}", description=f" \
                            Wygrał: **{winner.mention}**!\n\
                            Hostowany przez: {ctx.author.mention}",
                colour=discord.Colour.from_rgb(135, 255, 16))
            e.set_footer(text=f'Start: {time_start}')
            # e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png') Można wstawić tort(?) czy coś w tym stylu
            await ctx.send(f"Giveaway się zakończył! :tada:", embed=e)
            await ctx.send(f"Stwórz ticket na kanale <#838400969515597855>")


    @commands.command()
    async def ck(self, ctx):
        await ctx.message.delete()
        await ctx.author.send('Online')
    
    @commands.command(aliases=['offlinemode', 'offmode'])
    @commands.has_permissions(administrator=True)
    async def _offlinemode(self, ctx):
        await ctx.message.delete()
        await self.client.change_presence(status=discord.Status.invisible, activity=discord.Game(f"?pomoc"))
        await ctx.author.send("Jestem Teraz Offline.")


    @commands.command(aliases=['onlinemode', 'onmode'])
    @commands.has_permissions(administrator=True)
    async def _onlinemode(self, ctx):
        await ctx.message.delete()
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f"?pomoc"))
        await ctx.author.send("Jestem Teraz Online.")

def setup(client):
    client.add_cog(Admin_Commands(client))
