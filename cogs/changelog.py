import discord
import datetime
import asyncio
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

class Changelog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Bcolors.Green}{self.__class__.__name__}{Bcolors.ENDC} Cog has been loaded\n-----")
    
    @commands.command()
    async def changelog(self, ctx):
        v1_1 = discord.Embed(title="Update 1.1", description=f" \
                                    [+] Log update\n\
                                    [+] Liczenie zaproszeń\n\
                                    [+] Changelog\n\
                                    [/] Zmieniono działanie giveaway\n\
                                    [-] Usunięto błędy",
            colour=discord.Colour.from_rgb(135, 255, 16),
            timestamp=datetime.datetime.utcnow())
        v1_1.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        v1_1.set_footer(text='Wersia 1.1/1.2')
        v1_2 = discord.Embed(title="Update 1.2", description=f" \
                                    [+] Log update\n\
                                    [+] Komendy administracyjne\n\
                                    [+] Dodano naszą weryfikację\n\
                                    [/] Znowu zmieniono działanie giveaway\n\
                                    [-] Usunięto błędy",
            colour=discord.Colour.from_rgb(135, 255, 16),
            timestamp=datetime.datetime.utcnow())
        v1_2.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        v1_2.set_footer(text='Wersia 1.1/1.2')
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
        current = 0

        self.client.statute = [v1_1, v1_2]

        msg = await ctx.send(embed=self.client.statute[current])
        
        for button in buttons:
            await msg.add_reaction(button)
            
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=10.0)

            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break

            else:
                previous_page = current
                if reaction.emoji == u"\u23EA":
                    current = 0
                    
                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1
                        
                elif reaction.emoji == u"\u27A1":
                    if current < len(self.client.statute)-1:
                        current += 1

                elif reaction.emoji == u"\u23E9":
                    current = len(self.client.statute)-1

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=self.client.statute[current])

def setup(client):
    client.add_cog(Changelog(client))
