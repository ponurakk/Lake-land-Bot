import discord
import asyncio
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

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Bcolors.Green}{self.__class__.__name__}{Bcolors.ENDC} Cog has been loaded\n-----")
    
    @commands.command()
    async def regulamin(self, ctx):
        sPage1 = discord.Embed(title="1. Postanowienia ogólne", description=f" \
                                    `1.1` *Administracja może zmienić regulamin bez wcześniejszego poinformowania o tym graczy i/lub użytkowników discorda.*\n\
                                    `1.2` *Kary będą wymierzane zgodnie z zasadami serwera. Jedynym wyjątkiem jest: pkt. 1.4*\n\
                                    `1.3` *Nieznajomość regulaminu nie zwalnia cię z przestrzegania go*\n\
                                    `1.4` *Administracja ma prawo zawyżać kary w zależności od sytuacji.*",
            colour=discord.Colour.from_rgb(135, 255, 16),
            timestamp=datetime.datetime.utcnow())
        sPage1.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        sPage1.set_footer(text='Strona 1/4')
        sPage2 = discord.Embed(title="2. Rozgrywka na serwerze", description=f" \
                                    `2.1` *Zakaz posiadania wulgarnego, obraźliwego nicku*\n\
                                    `2.2` *Zakaz budowania budowli: obraźliwych, wulgarnych lub niezgodnych z powszechnie wyznawaną etyką.*\n\
                                    `2.3` *Działanie na szkodę serwera będzie karane.*\n\
                                    `2.4` *Zakaz jakiegokolwiek proszenia o rangi.*\n\
                                    `2.5` *Zakaz używania cheatów ani innych wspomagaczy (np. przezroczyste tekstury).*\n\
                                    `2.6` *Zakaz bugowania serwera, wykorzystywania błędów.*\n\
                                    `2.7` *Zakaz kopiowania itemów.*" ,
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow())
        sPage2.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        sPage2.set_footer(text='Strona 2/4')
        sPage3 = discord.Embed(title="3. Chat", description=f" \
                                    `3.1` *Zakaz nadużywania wulgaryzmów. Tyczy się to również wiadomości prywatnej.*\n\
                                    `3.2` *Zakaz obrażania graczy. Tyczy się to również wiadomości prywatnej.*\n\
                                    `3.3` *Zakaz floodowania. Flood jest to więcej niż 4 takie same znaki następujące po sobie.*\n\
                                    `3.4` *Zakaz pisania CAPSLOCKIEM.*\n\
                                    `3.5` *Zakaz spamowania.*\n\
                                    `3.6` *Zakaz zaśmiecania chatu.*\n\
                                    `3.7` *Zakaz pisania tekstów o treściach pornograficznych, nazistowskich, rasistowskich oraz innych tekstów/wyrazów/stwierdzeń niezgodnych z powszechnie wyznawaną etyką.*\n\
                                    `3.8` *Zakaz reklamowania innych serwerów (Strony WWW, Serwery MC, DC itp.)*\n\
                                    `3.9` *Zakaz używania znaków specjalnych w celu wyróżnienia swojej wiadomości.*\n\
                                    `3.10` *Zakaz umyślnego pisania niepoprawną polszczyzną.*\n\
                                    `3.11` *Zakaz obrażania serwera.*\n\
                                    `3.12` *Zakaz obrażania administracji serwera.*" ,
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow())
        sPage3.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        sPage3.set_footer(text='Strona 3/4')
        sPage4 = discord.Embed(title="4. Płatności", description=f" \
                                    `4.1` *W przypatku nie opłacenia 100% kwoty wymaganej, dotacja jest traktowna jako dobrowolny donate*\n\
                                    `4.2` *Płatności są realizowane za pomoca serwisu Tipply.pl*\n\
                                    `4.3` *W przypadku nie podania pełnych danych gracza przy składaniu zamówienia, dotacja jest traktowna jako dobrowolny donate.*" ,
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow())
        sPage4.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        sPage4.set_footer(text='Strona 4/4')

        self.client.statute = [sPage1, sPage2, sPage3, sPage4]
        

        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
        current = 0

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
    client.add_cog(Help(client))