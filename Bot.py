from genericpath import exists
import discord
import random
import asyncio
import datetime
import minestat
import prawcore
from prawcore import NotFound
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
    print('{0.user} is ready'.format(client))

    # ms = minestat.MineStat('lake-land.pl', 25565)
    # print('Minecraft server status of %s on port %d:' % (ms.address, ms.port))
    # if ms.online:
    #     print('Server is online running version %s with %s out of %s players.' % (ms.version, ms.current_players, ms.max_players))
    #     print('Message of the day: %s' % ms.motd)
    #     print('Message of the day without formatting: %s' % ms.stripped_motd)
    #     print('Latency: %sms' % ms.latency)
    #     print('Connected using protocol: %s' % ms.slp_protocol)
    # else:
    #     print('Server is offline!')
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

reddit = prawcore.Reddit(client_id='Qbi7Dac-PWQ2oD_X7uPxcQ',
                     client_secret='gmyMK1H9lawI861uML00AWOa0Omoyw',
                     user_agent='Meme finder', 
                     check_for_async=False)


@client.command()
async def meme(ctx, *, subreddit="memes"):

    exists = True
    try:
        reddit.subreddits.search_by_name(subreddit, exact=True)
    except NotFound:
        exists = False
    else:
        memes_submissions = reddit.subreddit(subreddit).hot()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        e = discord.Embed(title=f"{submission.title}l".format(client))
        e.set_image(url=submission.url)
        await ctx.message.delete()
        await ctx.send(embed=e)



# Help command

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
hPage2 = discord.Embed(title="Komendy LakeLand.pl".format(client), description=f" \
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
hPage3 = discord.Embed(title="Komendy LakeLand.pl".format(client), description=f" \
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

client.help_pages = [hPage1, hPage2, hPage3]

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

sPage1 = discord.Embed(title="Pomoc LakeLand.pl", description=f" \
                        **`?ip`** - Ip serwera\n\
                        **`?strona`** - Link do naszej strony\n\
                        **`?sklep`** - Link do naszego sklepu\n\
                        **`?fb`** - Link do naszego facebooka\n\
                        **`?dc`** - Link do naszego discorda" ,
        colour=discord.Colour.from_rgb(135, 255, 16),
        timestamp=datetime.datetime.utcnow())
sPage1.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
sPage1.set_footer(text='Strona 1/3')
sPage2 = discord.Embed(title="Pomoc LakeLand.pl", description=f" \
                        **`?ip`** - Ip serwera\n\
                        **`?strona`** - Link do naszej strony\n\
                        **`?sklep`** - Link do naszego sklepu\n\
                        **`?fb`** - Link do naszego facebooka\n\
                        **`?dc`** - Link do naszego discorda" ,
        colour=discord.Colour.from_rgb(135, 255, 16),
        timestamp=datetime.datetime.utcnow())
sPage2.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
sPage2.set_footer(text='Strona 1/3')
sPage3 = discord.Embed(title="Pomoc LakeLand.pl", description=f" \
                        **`?ip`** - Ip serwera\n\
                        **`?strona`** - Link do naszej strony\n\
                        **`?sklep`** - Link do naszego sklepu\n\
                        **`?fb`** - Link do naszego facebooka\n\
                        **`?dc`** - Link do naszego discorda" ,
        colour=discord.Colour.from_rgb(135, 255, 16),
        timestamp=datetime.datetime.utcnow())
sPage3.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
sPage3.set_footer(text='Strona 1/3')
sPage4 = discord.Embed(title="Pomoc LakeLand.pl", description=f" \
                        **`?ip`** - Ip serwera\n\
                        **`?strona`** - Link do naszej strony\n\
                        **`?sklep`** - Link do naszego sklepu\n\
                        **`?fb`** - Link do naszego facebooka\n\
                        **`?dc`** - Link do naszego discorda" ,
        colour=discord.Colour.from_rgb(135, 255, 16),
        timestamp=datetime.datetime.utcnow())
sPage4.set_thumbnail(url='https://lake-land.pl/unknown-removebg-preview.png')
sPage4.set_footer(text='Strona 1/3')

client.statute = [sPage1, sPage2, sPage3, sPage4]

@client.command()
async def regulamin(ctx):
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
    server = minestat.MineStat('feerko.pl', 25565)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"{server.current_players}/{server.max_players} Wbijaj na serwer!"))
    # Na razie jest tak potem może zmienie jak będzie działać


# Admin Commands

@client.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx, duration: int, time_type: str, *, prize: str):
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

    user_list = [u for u in await new_msg.reactions[0].users().flatten() if u != client.user] # Check the reactions/don't count the bot reaction

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
        await ctx.send(f'Niestety **{ctx.author.name}** ale nie jesteś Administratorem.')
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