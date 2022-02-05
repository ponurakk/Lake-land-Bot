import string
import discord
import datetime
import asyncio
import random
import time
import json
from discord.utils import get
from discord.ext import commands, tasks

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

class Giveaway(commands.Cog):

    def __init__(self, client):
        self.client = client
        # self.msg_id = 0
        # self.gend = time.time()
        # self.duration = 0
        # self.time_type = ""
        # self.prize = ""
        # self.channel = discord.channel
        # self.user = discord.user
    

    async def open_config(self, msg_id: int, gend: int, duration: int, time_type: string, prize: string, channel: discord.channel, user: discord.User):

        with open("./cogs/json/giveaway_config.json", "r") as f:
            data = json.load(f)

        data["msg_id"] = msg_id
        data["gend"] = gend
        data["duration"] = duration
        data["time_type"] = time_type
        data["prize"] = prize
        data["channel"] = channel
        data["user"] = user

        with open("./cogs/json/giveaway_config.json", "w") as f:
            json.dump(data, f, indent=4)
        return True

    async def get_config_data(self):
        with open("./cogs/json/giveaway_config.json", "r") as f:
            data = json.load(f)
        return data

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Bcolors.Green}{self.__class__.__name__}{Bcolors.ENDC} Cog has been loaded\n-----")
        self.run.start()

    @commands.command()
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def giveaway(self, ctx, duration: int, time_type: str, *, prize: str):
        # self.duration = duration
        # self.time_type = time_type
        # self.msg_id=msg.id
        # self.prize = prize
        # self.channel = ctx.channel
        # self.user = ctx.author
        # self.gend = int(time.time()+duration)

        await self.open_config(msg_id=ctx.message.id, gend=int(time.time()+duration), duration=duration, time_type=time_type, prize=prize, channel=ctx.channel.id, user=ctx.author.id)
        data = await self.get_config_data()

        gend = data["gend"]

        # ldigit = duration%10
        if time_type == 's':
            duration = duration
        elif time_type == 'm':
            duration = duration*60
        elif time_type == 'g':
            duration = duration*3600
        elif time_type == 'd':
            duration = duration*86400

        e = discord.Embed(title=prize,
                            description=f"Hostowany przez: {ctx.author.mention}\nZareaguj :tada: by dołączyć!\nKoniec giveaway'a: **<t:{gend}:R>**",
                            colour=discord.Colour.from_rgb(135, 255, 16),
                            timestamp=datetime.datetime.utcnow())

        msg = await ctx.channel.send(content=":tada: **GIVEAWAY** :tada:", embed=e)
        await msg.add_reaction("🎉")

        await self.open_config(msg_id=msg.id, gend=int(time.time()+duration), duration=duration, time_type=time_type, prize=prize, channel=ctx.channel.id, user=ctx.author.id)
        data = await self.get_config_data()
        
        self.run.start()

    @tasks.loop(seconds=1)
    async def run(self):
        data = await self.get_config_data()
        prize = data["prize"]
        msg_id = data["msg_id"]
        channel = data["channel"]
        user = get(self.client.get_all_members(), id=data["user"])

        channel = self.client.get_channel(channel)
        if data["gend"]==int(time.time()):
            new_msg = await channel.fetch_message(msg_id)

            user_list = [u for u in await new_msg.reactions[0].users().flatten() if u != self.client.user] # Check the reactions/don't count the bot reaction

            if len(user_list) == 0:
                await self.channel.send("Nikt nie zareagował. :7000squidpepe:")
            else:
                winner = random.choice(user_list)
                e = discord.Embed(title=f"{prize}", description=f" \
                                Wygrał: **{winner.mention}**!\n\
                                Hostowany przez: {user.mention}",
                    colour=discord.Colour.from_rgb(135, 255, 16))
                e.set_footer(text=f'Start: {int(time.time())}')
                # e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png') maybe put here some cake or sth
                await channel.send(f"Giveaway się zakończył! :tada:", embed=e)
                await channel.send(f"Stwórz ticket na kanale <#838400969515597855>")
                self.run.cancel()

def setup(client):
    client.add_cog(Giveaway(client))
