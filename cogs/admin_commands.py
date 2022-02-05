from turtle import color, title
import discord
import asyncio
import random
import datetime
import time
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

class Admin_Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Bcolors.Green}{self.__class__.__name__}{Bcolors.ENDC} Cog has been loaded\n-----")

    @commands.command()
    async def ck(self, ctx):
        await ctx.message.delete()
        await ctx.author.send('Online')

    @commands.command()
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def echo(self, ctx, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def clear(self, ctx, amount=1):
        if amount <= 1000:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send("Przepraszam ale liczba jest zbyt duża limit to **1000**.")

    @commands.command()
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def kick(self, ctx, member: discord.Member):
        msg = await ctx.send(f"Potwierdź usunięcie {member.name} z serwera.")
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        try:
            reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction1, user: user == ctx.author and reaction1.emoji in ['✅', '❌'], timeout=30.0)

        except asyncio.TimeoutError:
            await ctx.channel.send("Czas minął.")

        else:
            if reaction.emoji == '✅':
                await member.kick()
                await ctx.send(f"Pomyślnie wyrzucono")

            else:
                await ctx.channel.send("Ok")
    

    @commands.command()
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def dm(ctx, member: discord.Member, *, content):
        channel = await member.create_dm()
        await ctx.message.delete()
        await channel.send(content)

    @commands.command()
    @commands.has_any_role('Właściciel', 'Technik')
    async def spam(self, ctx, member: discord.Member, *, content):
        channel = await member.create_dm()
        await ctx.message.delete()
        i = 1
        while i <= 20:
            time.sleep(0.70)
            i += 1
            await channel.send(content)

    @commands.command()
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def ui(self, ctx, *, user: discord.User = None):
        if user is None:
            user = ctx.author
        e = discord.Embed(title=f"{user.name} info")
        e.add_field(name="ID:", value=user.id, inline=False)
        e.set_image(url=user.avatar_url)
        e.add_field(name="Is bot:", value=user.bot, inline=False)
        e.add_field(name="Represents Discord:", value=user.system, inline=False)
        e.add_field(name="Dm channel:", value=user.dm_channel, inline=False)
        e.add_field(name="User color:", value=user.color, inline=False)
        e.add_field(name="Account created:", value=user.created_at, inline=False)

        await ctx.send(embed=e)
    

    @commands.command()
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def welcome(self, ctx):
        e = discord.Embed(title=f"LakeLand.pl - Weryfikacja",
                        description=f"Aby uzyskać dostęp do kanałów, kliknij w reakcję weryfikacji!",
                        colour=discord.Colour.from_rgb(135, 255, 16))
        msg = await ctx.send(embed=e)
        await msg.add_reaction("✅")


    @commands.command()
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def mute(self, ctx, user: discord.Member):
        guild = ctx.guild
        role = discord.utils.get(guild.roles,name="mute")
        await user.add_roles(role)

    @commands.command()
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def unmute(self, ctx, user: discord.Member):
        guild = ctx.guild
        role = discord.utils.get(guild.roles,name="mute")
        await user.remove_roles(role)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        msg = await ctx.send(f"Potwierdź bana dla {member.name}.")
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        try:
            reaction, user = await self.client.wait_for("reaction_add", check=lambda reaction1, user: user == ctx.author and reaction1.emoji in ['✅', '❌'], timeout=30.0)

        except asyncio.TimeoutError:
            await ctx.channel.send("Czas minął.")

        else:
            if reaction.emoji == '✅':
                await member.ban(reason=reason)
                await ctx.send(f"Pomyślnie zbanowano użytkownika")

            else:
                await ctx.channel.send("Ok")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unnbaned {user.mention}")
                return
    
    @commands.command(aliases=['offlinemode', 'offmode'])
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def _offlinemode(self, ctx):
        await ctx.message.delete()
        await self.client.change_presence(status=discord.Status.invisible, activity=discord.Game(f"?pomoc"))
        await ctx.author.send("Jestem Teraz Offline.")


    @commands.command(aliases=['onlinemode', 'onmode'])
    @commands.has_any_role('Właściciel', 'Technik', 'Moderator', 'Helper')
    async def _onlinemode(self, ctx):
        await ctx.message.delete()
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f"?pomoc"))
        await ctx.author.send("Jestem Teraz Online.")

def setup(client):
    client.add_cog(Admin_Commands(client))
