import discord
import os
from discord.ext import commands, tasks
import git

intents = discord.Intents.default().all()
client = commands.Bot(command_prefix="?", intents=intents)
token = open("token2", "r").read() # token to nazwa pliku z tokenem XD
intents.members = True
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

@client.event
async def on_ready():
    print('{0.user} is ready'.format(client))

    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"?pomoc"))
    run.start()

repo = git.Repo(".git")
repo.remotes.origin.pull("Stable-release")
@tasks.loop(seconds=5)
async def run():
    current = repo.head.commit
    repo.remotes.origin.pull("Stable-release")
    if current != repo.head.commit:
        print("Updated to newest version.")

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