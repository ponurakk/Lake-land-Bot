from pydoc import cli
import discord
import random
import json
from discord.ext import tasks
from discord.ext import commands
from mcstatus import MinecraftServer


client = commands.Bot(command_prefix="?")
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
        await message.channel.send('Hej. Mój prefix to `;`')
    if message.content == "ping":
        await message.channel.send('**Pong**')
        ping_ = client.latency
        ping = round(ping_ * 1000)
        print(f'Ping: {Bcolors.Green}{ping}{Bcolors.ENDC}')
        await message.channel.send(f"My ping is {ping}ms")

    await client.process_commands(message)

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
async def giveaway(ctx, *, topic, ):
    await ctx.send(':4698peperespected: GIVEAWAY :4698peperespected:')
    embed = discord.Embed(title=topic)
    embed.add_field(name=topic, value='', inline=False)
    embed.footer(name='a', value='')
    guild = ctx.guild
    random.random = guild.users

    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def ck(ctx):
    await ctx.message.delete()
    await ctx.author.send('Online')

@client.command(aliases=['offlinemode', 'offmode'])
@commands.has_permissions(administrator=True)
async def _offlinemode(ctx):
    await ctx.message.delete()
    await client.change_presence(status=discord.Status.invisible, activity=discord.Game("U don't even see me"))
    await ctx.author.send("Jestem Teraz Offline.")


@client.command(aliases=['onlinemode', 'onmode'])
@commands.has_permissions(administrator=True)
async def _onlinemode(ctx):
    await ctx.message.delete()
    await client.change_presence(status=discord.Status.online, activity=discord.Game('122 032 119 032 065'))
    await ctx.author.send("Jestem Teraz Online.")

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