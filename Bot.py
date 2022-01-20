import discord
import random
import asyncio
import datetime
import praw
import os
from prawcore import NotFound
from discord.ext import commands


client = commands.Bot(command_prefix="?")
token = open("token2", "r").read() # token to nazwa pliku z tokenem XD

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

    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"?pomoc"))


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension}')
    print(f'{Bcolors.Green}{extension}{Bcolors.ENDC} loaded by {ctx.author.name}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded {extension}')
    print(f'{Bcolors.Red}{extension}{Bcolors.ENDC} unloaded by {ctx.author.name}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded {extension}')
    print(f'{Bcolors.Yellow}{extension}{Bcolors.ENDC} reloaded by {ctx.author.name}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Commands

reddit = praw.Reddit(client_id='Qbi7Dac-PWQ2oD_X7uPxcQ',
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

        e = discord.Embed(title=f"{submission.title}".format(client),
                          colour=discord.Colour.from_rgb(135, 255, 16))
        e.set_image(url=submission.url)
        await ctx.message.delete()
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