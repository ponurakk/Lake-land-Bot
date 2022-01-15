from dis import dis, disco
from email import message
from pydoc import cli
from time import time
from turtle import color, title
import discord
import random
import asyncio
import datetime
from discord.ext import tasks
from discord.ext import commands
from mcstatus import MinecraftServer


client = commands.Bot(command_prefix="?", help_command=None)
token = open("token", "r").read() # token to nazwa pliku z tokenem XD

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

# Events

@client.event
async def on_ready():
    
    change_status.start()
    print('{0.user} is ready'.format(client))

    server = MinecraftServer('lake-land.pl')
    status = server.status()
    latency = server.ping()
    print(f"The server replied in {latency} ms")
    query = server.query()
    print(f"The server has the following players online: {', '.join(query.players.names)}")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"{status.players.online}/{status.players.max} Wbijaj na serwer!"))
    # Na razie jest tak potem może zmienie jak będzie działać


# Commands
@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send(f'Hej. Mój prefix to `{client.command_prefix}`')
    if message.content == "ping":
        await message.channel.send('**Pong**')
        ping_ = client.latency
        ping = round(ping_ * 1000)
        print(f'Ping: {Bcolors.Green}{ping}{Bcolors.ENDC}')
        e = discord.Embed(client)
        await message.channel.send(f"My ping is {ping}ms")

    await client.process_commands(message)


page1 = discord.Embed(title="Pomoc LakeLand.pl", description=f" \
                        **`?ip`** - Ip serwera\n\
                        **`?strona`** - Link do naszej strony\n\
                        **`?sklep`** - Link do naszego sklepu\n\
                        **`?fb`** - Link do naszego facebooka\n\
                        **`?dc`** - Link do naszego discorda" ,
        colour=discord.Colour.from_rgb(135, 255, 16),
        timestamp=datetime.datetime.utcnow())
page1.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
page1.set_footer(text='Strona 1/2')
page2 = discord.Embed(title="Komendy LakeLand.pl".format(client), description=f" \
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
page2.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
page2.set_footer(text='Strona 2/2')

client.help_pages = [page1, page2]

@client.command()
async def pomoc(ctx, *, command=None):
    if command == None:
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
        current = 0

        msg = await ctx.send(embed=client.help_pages[current])
        
        for button in buttons:
            await msg.add_reaction(button)
            
        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=10.0)

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
                    if current < len(client.help_pages)-1:
                        current += 1

                elif reaction.emoji == u"\u23E9":
                    current = len(client.help_pages)-1

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=client.help_pages[current])
    elif command == "ip":
        e = discord.Embed(title="Pomoc {0.user}".format(client), description="Ip naszego serwera minecraft\n`lake-land.pl`", colour=discord.Colour.from_rgb(135, 255, 16), timestamp=datetime.datetime.utcnow())
        e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        await ctx.send(embed=e)
    elif command == "strona":
        e = discord.Embed(title="Pomoc {0.user}".format(client), description="Link do naszej strony\nhttps://lake-land.pl", colour=discord.Colour.from_rgb(135, 255, 16), timestamp=datetime.datetime.utcnow())
        e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        await ctx.send(embed=e)
    elif command == "sklep":
        e = discord.Embed(title="Pomoc {0.user}".format(client), description="Link do naszego sklepu\nhttps://lake-land.pl/shop/Survival", colour=discord.Colour.from_rgb(135, 255, 16), timestamp=datetime.datetime.utcnow())
        e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        await ctx.send(embed=e)
    elif command == "fb":
        e = discord.Embed(title="Pomoc {0.user}".format(client), description="Link do naszego facebooka\nhttps://fb.lake-land.pl", colour=discord.Colour.from_rgb(135, 255, 16), timestamp=datetime.datetime.utcnow())
        e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        await ctx.send(embed=e)
    elif command == "dc":
        e = discord.Embed(title="Pomoc {0.user}".format(client), description="Link do naszego discorda\nhttps://dc.lake-land.pl", colour=discord.Colour.from_rgb(135, 255, 16), timestamp=datetime.datetime.utcnow())
        e.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
        await ctx.send(embed=e)


@client.command()
async def ip(ctx):
    await ctx.send('IP Serwera: lake-land.pl')

@client.command()
async def strona(ctx):
    await ctx.send('Strona internetowa: https://lake-land.pl')

@client.command()
async def sklep(ctx):
    await ctx.send('Sklep: https://lake-land.pl/shop/Survival')

@client.command()
async def fb(ctx):
    await ctx.send('Facebook: https://fb.lake-land.pl')

@client.command()
async def dc(ctx):
    await ctx.send('Discord: https://dc.lake-land.pl')


@tasks.loop(seconds=5)
async def change_status():
    server = MinecraftServer('lake-land.pl')
    status = server.status()
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"{status.players.online}/{status.players.max} Wbijaj na serwer!"))
    # Na razie jest tak potem może zmienie jak będzie działać


# Admin Commands

@client.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx, duration: int, time_type: str, *, prize: str):
    ldigit = duration%10
    if time_type == 's':
        time_name = 'sekuny'
    elif time_type == 'm':
        time_name = 'minuty'
    elif time_type == 'g':
        time_name = 'godziny'
    elif time_type == 'd':
        time_name = 'dni'
    
    embed = discord.Embed(title=prize,
                        description=f"Hostowany przez: {ctx.author.mention}\nZareaguj :tada: by dołączyć!\nPozostały czas: **{duration}** {time_name}",
                        color=ctx.guild.me.top_role.color, )

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

    user_list = [u for u in await new_msg.reactions[0].users().flatten() if u != client.user] # Check the reactions/don't count the bot reaction

    if len(user_list) == 0:
        await ctx.send("Nikt nie zareagował. :7000squidpepe:") 
    else:
        winner = random.choice(user_list)
        e = discord.Embed()
        e.title = winner.mention
        e.description = f"Wygrałeś: **{prize}**!"
        e.description = f"Hostowany przez: {ctx.author.mention}"
        e.timestamp = datetime.datetime.utcnow()
        await ctx.send(f"Giveaway się zakończył! :tada:", embed=e)
        await ctx.send(f"Stwórz ticket na {client.get_channel}#「📩」ticket ")


@client.command()
@commands.has_permissions(administrator=True)
async def ck(ctx):
    await ctx.message.delete()
    await ctx.author.send('Online')

# @client.command(aliases=['offlinemode', 'offmode'])
# @commands.has_permissions(administrator=True)
# async def _offlinemode(ctx):
#     await ctx.message.delete()
#     await client.change_presence(status=discord.Status.invisible, activity=discord.Game("U don't even see me"))
#     await ctx.author.send("Jestem Teraz Offline.")


# @client.command(aliases=['onlinemode', 'onmode'])
# @commands.has_permissions(administrator=True)
# async def _onlinemode(ctx):
#     await ctx.message.delete()
#     await client.change_presence(status=discord.Status.online, activity=discord.Game('122 032 119 032 065'))
#     await ctx.author.send("Jestem Teraz Online.")

# Error handlers

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Najpierw spełnij wszystkie wymagania.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send(f'Niestety ale nie jesteś Administratorem. **{ctx.author.name}**')
    if isinstance(error, commands.TooManyArguments):
        await ctx.send('Wpisałeś zbyt dużo argumentów.')
    if isinstance(error, commands.ChannelNotFound):
        await ctx.send('Nie ma takiego kanału.')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send('Niestety nie posiadasz odpowiedniej roli.')
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Nie ma takiego użytkownika.')
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Aby wykonać tą komendę ponownie poczekaj **{:.2f}**'.format(error.retry_after)
        await ctx.send(msg, delete_after=error.retry_after)

client.run(token)