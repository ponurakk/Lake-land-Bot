import discord
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

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Bcolors.Green}Events{Bcolors.ENDC} loaded')
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            e = discord.Embed(
                title="",
                description=f"**Wiadomość wysłana przez {message.author.mention} usunięta w {message.channel.mention}.**\n\
                    `{message.content}`",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow())

            e.set_author(name=message.author,
                icon_url=message.author.avatar_url)

            e.set_footer(text=f'{message.guild.name}')


            channel = self.client.get_channel(804447582167629824) # 804447582167629824 836494084104781847
            await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if not message_before.author.bot:
            e = discord.Embed(
                title="",
                description=f"**Wiadomość wysłana przez {message_before.author.mention} edytowana w {message_before.channel.mention}.** [Skocz do wiadomości.]({message_before.jump_url})\n\
                    **Przed:**\n\
                    `{message_before.content}`\n\
                    **Po:**\n\
                    `{message_after.content}`",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow())
            e.set_author(name=message_before.author,
                icon_url=message_before.author.avatar_url)

            e.set_footer(text=f'{message_before.guild.name}')


            channel = self.client.get_channel(804447582167629824) # 804447582167629824 836494084104781847
            await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.mentioned_in(message):
            await message.channel.send(f'Hej. Mój prefix to `{self.client.command_prefix}`')
        if message.content == "ping":
            await message.channel.send('**Pong**')
            ping_ = self.client.latency
            ping = round(ping_ * 1000)
            print(f'Ping: {Bcolors.Green}{ping}{Bcolors.ENDC}')
            await message.channel.send(f"My ping is {ping}ms")

def setup(client):
    client.add_cog(Events(client))

        
# discord.on_message_delete(message)
# discord.on_message_edit(before, after)
# discord.on_reaction_add(reaction, user)
# discord.on_guild_channel_delete(channel)
# discord.on_guild_channel_create(channel)
# discord.on_guild_channel_update(before, after)
# discord.on_member_join(member) # nie wiem czy trzeba ¯\_(ツ)_/¯
# discord.on_member_remove(member) # nie wiem czy trzeba ¯\_(ツ)_/¯
# discord.on_member_update(before, after)
# discord.on_guild_role_create(role)
# discord.on_guild_role_delete(role)
# discord.on_guild_role_update(before, after)
# discord.on_member_ban(guild, user)
# discord.on_member_unban(guild, user)
# discord.on_invite_create(invite)
# discord.on_invite_delete(invite)
# discord.on_group_join(channel, user)
# discord.on_group_remove(channel, user)