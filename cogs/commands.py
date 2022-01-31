from http import client
from re import I
import discord
import praw
import random
import json
import datetime
from prawcore import NotFound
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

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Bcolors.Green}{self.__class__.__name__}{Bcolors.ENDC} Cog has been loaded\n-----")



    @commands.command()
    async def meme(self, ctx, *, subreddit="memes"):    
        reddit = praw.Reddit(client_id='Qbi7Dac-PWQ2oD_X7uPxcQ',
                        client_secret='gmyMK1H9lawI861uML00AWOa0Omoyw',
                        user_agent='Meme finder', 
                        check_for_async=False)

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

            e = discord.Embed(title=f"{submission.title}".format(self.client),
                            colour=discord.Colour.from_rgb(135, 255, 16))
            e.set_image(url=submission.url)
            await ctx.message.delete()
            await ctx.send(embed=e)

    @commands.command()
    async def ip(self, ctx):
        await ctx.send('IP Serwera: lake-land.pl')

    @commands.command()
    async def strona(self, ctx):
        await ctx.send('Strona internetowa: https://lake-land.pl')

    @commands.command()
    async def sklep(self, ctx):
        await ctx.send('Sklep: https://lake-land.pl/shop/Survival')

    @commands.command()
    async def fb(self, ctx):
        await ctx.send('Facebook: https://fb.lake-land.pl')

    @commands.command()
    async def dc(self, ctx):
        await ctx.send('Discord: https://dc.lake-land.pl')

    async def get_profile_data(self):
        with open("cogs/json/invites.json", "r") as f:
            users = json.load(f)
        return users
    
    async def open_account(self, user):
        with open("cogs/json/invites.json", "r") as f:
            users = json.load(f)

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["Nick"] = user.name
            users[str(user.id)]["Total"] = 0
            users[str(user.id)]["Invites"] = 0
            users[str(user.id)]["Leaves"] = 0
            users[str(user.id)]["Invited_Players"] = []

        with open("cogs/json/invites.json", "w") as f:
            json.dump(users, f, indent=4)
            # TODO: sort_keys=True / sortuje alfabetycznie(nie polecam) # nie sortuje nazwy użytkownika ale daje na koniec
        return True

    @commands.command()
    async def invites(self, ctx):
        await self.open_account(ctx.author)
        user = ctx.author
        users = await self.get_profile_data()

        total = users[str(user.id)]["Total"]
        invites = users[str(user.id)]["Invites"]
        leaves = users[str(user.id)]["Leaves"]
        e = discord.Embed(
            title=f"Statystyki zaproszeń dla {ctx.author.name}",
            description=f"{ctx.author.mention} ma **{total}** zaproszeń!\n\n\
                ✅ {invites} normalnych\n\
                🚫 {leaves} wyszło",
            colour=discord.Colour.from_rgb(135, 255, 16),
            timestamp=datetime.datetime.utcnow()
            )
        e.set_footer(text=f'{ctx.author.name}')
        e.set_thumbnail(url=ctx.author.avatar_url)
        e.set_footer(icon_url=self.client.user.avatar_url, text=ctx.author)
        await ctx.send(embed=e)

    @commands.command()
    async def total(self, ctx):

        guild = self.client.get_guild(779319110885965844)
        await ctx.send(f"Liczba członków: {ctx.guild.member_count}")
        for members in guild.members:

            await self.open_account(members)
            user = members
            users = await self.get_profile_data()
            
            print(members.name)
            users[str(user.id)]["Total"] = 0
            users[str(user.id)]["Invites"] = 0
            users[str(user.id)]["Leaves"] = 0
            users[str(user.id)]["Invited_Players"] = []

def setup(client):
    client.add_cog(Commands(client))
