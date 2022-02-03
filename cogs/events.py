import discord
import datetime
import DiscordUtils
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
        print(f"{Bcolors.Green}{self.__class__.__name__}{Bcolors.ENDC} Cog has been loaded\n-----")
    
    # message

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            e = discord.Embed(
                title="",
                description=f"**Wiadomość wysłana przez {message.author.mention} usunięta w {message.channel.mention}.**\n\
                    `{message.content}`",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow()
            )

            e.set_author(name=message.author,
                icon_url=message.author.avatar_url)

            e.set_footer(text=f'{message.guild.name}')


            channel = self.client.get_channel(836494084104781847) # 804447582167629824 836494084104781847
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
                timestamp=datetime.datetime.utcnow()
            )
            e.set_author(name=message_before.author,
                icon_url=message_before.author.avatar_url)

            e.set_footer(text=f'{message_before.guild.name}')


            channel = self.client.get_channel(836494084104781847) # 804447582167629824 836494084104781847
            await channel.send(embed=e)
    
    # channel

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        e = discord.Embed(
                title="",
                description=f"Usunięto kanał #{channel.name}",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow()
        )
        e.set_author(name=channel.name)

        e.set_footer(text=f'{channel.guild.name}')


        channel = self.client.get_channel(836494084104781847) # 804447582167629824 836494084104781847
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        e = discord.Embed(
                title="",
                description=f"Stworzono kanał {channel.mention}",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow()
        )
        e.set_author(name=channel.name)

        e.set_footer(text=f'{channel.guild.name}')


        channel = self.client.get_channel(836494084104781847) # 804447582167629824 836494084104781847
        await channel.send(embed=e)
    
    @commands.Cog.listener()
    async def on_guild_channel_update(self, channel_before, channel_after):
        if channel_before.name != channel_after.name and channel_before.topic == channel_after.topic:
            e = discord.Embed(
                title="",
                description=f"**Nazwa {channel_after.mention} została edytowana.**\n\
                    **Z:**\n\
                    `{channel_before.name}`\n\
                    **Na:**\n\
                    `{channel_after.name}`",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow()
            )
            e.set_author(name=channel_before.guild.name,
                        icon_url=channel_before.guild.icon_url)

            e.set_footer(text=f'{channel_before.guild.name}') 
        elif channel_before.topic != channel_after.topic and channel_before.name == channel_after.name:
            e = discord.Embed(
                title="",
                description=f"**Temat kanału {channel_after.mention} został edytowany.**\n\
                    **Przed:**\n\
                    `{channel_before.topic}`\n\
                    **Po:**\n\
                    `{channel_after.topic}`",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow()
            )
            e.set_author(name=channel_before.guild.name,
                        icon_url=channel_before.guild.icon_url)

            e.set_footer(text=f'{channel_before.guild.name}')
        elif channel_before.topic != channel_after.topic and channel_before.name != channel_after.name:
            e = discord.Embed(
                title="",
                description=f"**Nazwa i temat kanału {channel_after.mention} zostały edytowane.**\n\
                    **Nazwa Przed:**\n\
                    `{channel_before.name}`\n\
                    **Nazwa Po:**\n\
                    `{channel_after.name}`\n\
                    **Temat Przed:**\n\
                    `{channel_before.topic}`\n\
                    **Temat Po:**\n\
                    `{channel_after.topic}`",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow()
            )
            e.set_author(name=channel_before.guild.name,
                        icon_url=channel_before.guild.icon_url)

            e.set_footer(text=f'{channel_before.guild.name}')

        channel = self.client.get_channel(836494084104781847) # 804447582167629824 836494084104781847
        await channel.send(embed=e)

    # member

    @commands.Cog.listener()
    async def on_member_join(self, member):
        e = discord.Embed(
                title="",
                description=f"**Do serwera dołączył {member.mention}.**",
                colour=discord.Colour.from_rgb(135, 255, 16),
                timestamp=datetime.datetime.utcnow()
        )
        e.add_field(name="ID:", value=member.id, inline=False)
        e.add_field(name="Konto stworzone:", value=member.created_at, inline=False)
        e.set_author(name=member.name,
                    icon_url=member.avatar_url)

        channel = self.client.get_channel(836494084104781847) # 804447582167629824 836494084104781847
        await channel.send(embed=e)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        e = discord.Embed(
                title="",
                description=f"**Własnie wyszedł {member.mention}.**",
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow()
        )
        e.add_field(name="ID:", value=member.id, inline=False)
        e.add_field(name="Dołączył:", value=member.joined_at, inline=False)
        e.set_author(name=member.name,
                    icon_url=member.avatar_url)
        
        channel = self.client.get_channel(836494084104781847) # 804447582167629824 836494084104781847
        await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        e = discord.Embed(
                title="",
                description=f"**Użytkownik {user.mention} został zbabnowany.**",
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow()
        )
        e.add_field(name="ID:", value=user.id, inline=False)
        e.set_author(name=user.name,
                    icon_url=user.avatar_url)
        
        channel = self.client.get_channel(836494084104781847) # 804447582167629824 836494084104781847
        await channel.send(embed=e)
    
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        e = discord.Embed(
                title="",
                description=f"**Użytkownik {user.mention} został odbanowany.**",
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow()
        )
        e.add_field(name="ID:", value=user.id, inline=False)
        e.set_author(name=user.name,
                    icon_url=user.avatar_url)

        channel = self.client.get_channel(836494084104781847) # 804447582167629824 836494084104781847
        await channel.send(embed=e)
    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id == 836926775204249610:
            if str(payload.emoji) == "✅":
                role = discord.utils.get(payload.member.guild.roles, name="Gracz")
                await payload.member.add_roles(role)
        if payload.channel_id == 925001167375831120:
            if payload.message_id == 925001167375831120:
                if str(payload.emoji) == "🔧":
                    role = discord.utils.get(payload.member.guild.roles, name="changelog")
                    await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_message(self, message):
        hello = ["hello", "hi", "witam", "siema"]
        if self.client.user.mentioned_in(message):
            await message.channel.send(f'Hej. Mój prefix to `{self.client.command_prefix}`')
        admin = discord.utils.find(lambda r: r.name == 'Właściciel', message.guild.roles)
        technik = discord.utils.find(lambda r: r.name == 'Technik', message.guild.roles)
        mod = discord.utils.find(lambda r: r.name == 'Moderator', message.guild.roles)
        helper = discord.utils.find(lambda r: r.name == 'Helper', message.guild.roles)
        opiekun = discord.utils.find(lambda r: r.name == 'Opiekun', message.guild.roles)

        if message.content == "ping" and ((admin in message.author.roles) or (technik in message.author.roles) or (mod in message.author.roles) or (helper in message.author.roles) or (opiekun in message.author.roles)):
            await message.channel.send('**Pong**')
            ping_ = self.client.latency
            ping = round(ping_ * 1000)
            print(f'Ping: {Bcolors.Green}{ping}{Bcolors.ENDC}')
            await message.channel.send(f"My ping is {ping}ms")

        if message.content in hello:
            await message.channel.send(f"Witaj.")

        if message.content == "huj":
            await message.channel.send(f"*chuj")

def setup(client):
    client.add_cog(Events(client))

        
# discord.on_message_delete(message) +
# discord.on_message_edit(before, after) +
# discord.on_reaction_add(reaction, user) ¯\_(ツ)_/¯
# discord.on_guild_channel_delete(channel) +
# discord.on_guild_channel_create(channel) +
# discord.on_guild_channel_update(before, after) +
# discord.on_member_join(member) +
# discord.on_member_remove(member) +
# discord.on_member_update(before, after) -
# discord.on_guild_role_create(role) -
# discord.on_guild_role_delete(role) -
# discord.on_guild_role_update(before, after) -
# discord.on_member_ban(guild, user) +
# discord.on_member_unban(guild, user) +
# discord.on_invite_create(invite) -
# discord.on_invite_delete(invite) -
# discord.on_group_join(channel, user) -
# discord.on_group_remove(channel, user) -