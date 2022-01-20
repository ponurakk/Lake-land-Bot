from turtle import title
import discord
import datetime
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

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

guild_ids = [779319110885965844]

class Slash(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Bcolors.Green}Slash{Bcolors.ENDC} loaded')
    
    @cog_ext.cog_slash(
        name="media", 
        guild_ids=guild_ids, 
        description="Dołącz do naszych mediów.",
        options=[
                create_option(
                    name="nick",
                    description="Nick w Minecraft.",
                    option_type=3,
                    required=True
                ),
                create_option(
                    name="rodzaj",
                    description="TikTok/YouTube.",
                    option_type=3,
                    required=True,
                    choices=[
                        create_choice(
                            name="YouTube",
                            value="YouTube"
                        ),
                        create_choice(
                            name="Twitch",
                            value="Twitch"
                        ),
                        create_choice(
                            name="TikTok",
                            value="TikTok"
                        )
                    ]
               ),
               create_option(
                 name="liczba",
                 description="Subskrypcji/Obserwacji.",
                 option_type=4,
                 required=True
               ),
               create_option(
                 name="link",
                 description="do kanału na Tiktok/YouTube/Twitch.",
                 option_type=3,
                 required=True
               ),
               create_option(
                 name="srednia",
                 description="Średnia liczba wyświetleń filmów.",
                 option_type=4,
                 required=True
               )
             ]
    )
    async def _media(self, ctx, nick: str, rodzaj: str, liczba: int, link: str, srednia: int):
        links = ['https://www.youtube.com/', 'https://vm.tiktok.com/', 'https://www.tiktok.com/',
                 'https://www.twitch.tv/']
        if any(word in link for word in links):
            e = discord.Embed(title=f"Informacje użytkownika {ctx.author.name}.", description=f" \
                            Nick w Minecraft: **{nick}**\n\
                            Typ Kanału: **{rodzaj}**\n\
                            Liczba sub/obs: **{liczba}**\n\
                            Link do kanału: **{link}**\n\
                            Średnia liczba wyświetleń: **{srednia}**",
            colour=discord.Colour.from_rgb(135, 255, 16),
            timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=e)
        else:
            await ctx.send('Podałeś zły link.')

def setup(client):
    client.add_cog(Slash(client))
