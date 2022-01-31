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
    async def pomoc(self, ctx, *, command=None):
        hPage1 = discord.Embed(title="Pomoc LakeLand.pl", description=f" \
                        **`?ip`** - Ip serwera\n\
                        **`?strona`** - Link do naszej strony\n\
                        **`?sklep`** - Link do naszego sklepu\n\
                        **`?fb`** - Link do naszego facebooka\n\
                        **`?dc`** - Link do naszego discorda" ,
        colour=discord.Colour.from_rgb(135, 255, 16),
        timestamp=datetime.datetime.utcnow())
        hPage1.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        hPage1.set_footer(text='Strona 1/3')
        hPage2 = discord.Embed(title="Komendy LakeLand.pl".format(self.client), description=f" \
                                **`/register <hasło> <hasło>`** - Rejstracja\n\
                                **`/l <hasło> | /login <hasło>`** - Logowanie\n\
                                **`/changepassword <stare Hasło> <nowe Hasło>`** - Zmień hasło\n\
                                **`/msg <gracz> | /wiadomosc <gracz>`** - Prywatna wiadomość\n\
                                **`/r <message> | /reply`** - Odpowiedź na ostatnią wiadomość prywatną\n\
                                **`/workbench`** - Crafting (Wyłącznie dla **Vip+**)\n\
                                **`/warp`** - Teleport do warpów\n\
                                **`/kosz`** - Poprostu kosz\n\
                                **`/trade <gracz>`** - Rozpoczęcie wymiany z innym graczem\n\
                                **`/trade accept/deny`** - Akceptacja lub odrzucanie wymiany\n\
                                **`/tpa <gracz>`** - Teleportacja do gracza\n\
                                **`/tpaaccept`** - Akceptacja teleportacji\n\
                                **`/tpadeny`** - Odrzucanie teleportacji\n\
                                **`/spawn`** - Teleportacja na spawn\n\
                                **`/sethome | /ustawdom`** - Ustaw dom\n\
                                **`/delhome <nazwa>`** - Usuń dom\n\
                                **`/home | /dom`** - Twoje dostępne domy\n\
                                **`/delhome <nazwa>`** - Usuń dom\n\
                                **`/kasa | /konto`** - Ilość twoich pieniadzy.\n\
                                **`/przelew <nazwa> | /przelej <nazwa>`** - Przelej pieniądze do gracza.\n\
                                **`/backpack`** - Plecak.\n\
                                **`/sklep | /discord | /strona`** - Link do social mediów.\n\
                                **`/rynek`** - Rynek\n\
                                **`/aukcje`** - Aukcje\n\
                                **`/ah`** - Sklep/Rynek graczy\n\
                                **`/domaukcyjny`** - Dom aukcyjny\n\
                                **`/dzialka`** - lista komend dzialki\n\
                                **`/skup | /market`** - Skup serwerowy\n\
                                **`/sprzedajwszytsko lub /sprzedajgui`** - Sprzedaj wszystkie przedmioty\n",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow())
        hPage2.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        hPage2.set_footer(text='Strona 2/3')
        hPage3 = discord.Embed(title="Komendy LakeLand.pl".format(self.client), description=f" \
                                **`/dzialka info | /dinfo`** - Informacje na teamt działki\n\
                                **`/dzialka add <nick>`** - Dodawanie do działki\n\
                                **`/dzialka remove <nick>`** - Usuwanie z działki\n\
                                **`/dzialka name`** - Ustawianie nazwy działki\n\
                                **`/dzialka polacz`** - łączenie działek\n\
                                **`/dzialka flag`** - flagi działek\n\
                                **`/dzialka get`** - Odebranie działki (200$)\n\
                                **`/dzialka home`** - Teleport do działki\n\
                                **`/dzialka sethome`** - Ustawienie home działki\n\
                                **`/dzialka granica`** - Granica działki\n\
                                **`/dzialka view`** - Granice działki\n\
                                **`/dzialka unclaim`** - Usuwanie działki\n\
                                **`/dzialka toggle`** - Blokada działki",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow())
        hPage3.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        hPage3.set_footer(text='Strona 3/3')

        self.client.help_pages = [hPage1, hPage2, hPage3]
        
        if command == None:
            buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
            current = 0

            msg = await ctx.send(embed=self.client.help_pages[current])
            
            for button in buttons:
                await msg.add_reaction(button)
                
            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=20.0)

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
                        if current < len(self.client.help_pages)-1:
                            current += 1

                    elif reaction.emoji == u"\u23E9":
                        current = len(self.client.help_pages)-1

                    for button in buttons:
                        await msg.remove_reaction(button, ctx.author)

                    if current != previous_page:
                        await msg.edit(embed=self.client.help_pages[current])
        elif command == "ip":
            e = discord.Embed(title="Pomoc {0.user}".format(self.client), description="Ip naszego serwera minecraft\n`lake-land.pl`", colour=discord.Colour.from_rgb(135, 255, 16), timestamp=datetime.datetime.utcnow())
            e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
            await ctx.send(embed=e)
        elif command == "strona":
            e = discord.Embed(title="Pomoc {0.user}".format(self.client), description="Link do naszej strony\nhttps://lake-land.pl", colour=discord.Colour.from_rgb(135, 255, 16), timestamp=datetime.datetime.utcnow())
            e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
            await ctx.send(embed=e)
        elif command == "sklep":
            e = discord.Embed(title="Pomoc {0.user}".format(self.client), description="Link do naszego sklepu\nhttps://lake-land.pl/shop/Survival", colour=discord.Colour.from_rgb(135, 255, 16), timestamp=datetime.datetime.utcnow())
            e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
            await ctx.send(embed=e)
        elif command == "fb":
            e = discord.Embed(title="Pomoc {0.user}".format(self.client), description="Link do naszego facebooka\nhttps://fb.lake-land.pl", colour=discord.Colour.from_rgb(135, 255, 16), timestamp=datetime.datetime.utcnow())
            e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
            await ctx.send(embed=e)
        elif command == "dc":
            e = discord.Embed(title="Pomoc {0.user}".format(self.client), description="Link do naszego discorda\nhttps://dc.lake-land.pl", colour=discord.Colour.from_rgb(135, 255, 16), timestamp=datetime.datetime.utcnow())
            e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
            await ctx.send(embed=e)

def setup(client):
    client.add_cog(Help(client))
