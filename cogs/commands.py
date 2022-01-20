import discord
import praw
import random
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
        print(f'{Bcolors.Green}Commands{Bcolors.ENDC} loaded')



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

def setup(client):
    client.add_cog(Commands(client))
