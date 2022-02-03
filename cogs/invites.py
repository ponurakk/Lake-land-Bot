import json
from discord.ext import commands
# from discord.ext.commands import has_permissions
from discord import Embed

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

class Invite_tracker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logs_channel = 804447582167629824

        self.invites = {}
        client.loop.create_task(self.load())

    async def load(self):
        await self.client.wait_until_ready()
        # load the invites
        for guild in self.client.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except:
                pass

    def find_invite_by_code(self, inv_list, code):
        for inv in inv_list:
            if inv.code == code:
                return inv


    async def get_profile_data(self):
        with open("./cogs/json/invites.json", "r") as f:
            users = json.load(f)
        return users

    async def open_account(self, user):

        with open("./cogs/json/invites.json", "r") as f:
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

        with open("./cogs/json/invites.json", "w") as f:
            json.dump(users, f, indent=4)
            # TODO: sort_keys=True / sortuje alfabetycznie(nie polecam) # nie sortuje nazwy użytkownika ale daje na koniec
        return True
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Bcolors.Green}{self.__class__.__name__}{Bcolors.ENDC} Cog has been loaded\n-----")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.open_account(member)
        user = member
        users = await self.get_profile_data()
        logs = self.client.get_channel(int(self.logs_channel))
        try:
            invs_before = self.invites[member.guild.id]
            invs_after = await member.guild.invites()
            self.invites[member.guild.id] = invs_after
            for invite in invs_before:
                if invite.uses < self.find_invite_by_code(invs_after, invite.code).uses:
                    users[str(invite.inviter.id)]["Invites"] += 1
                    users[str(invite.inviter.id)]["Invited_Players"].append(str(member.id))
                    users[str(invite.inviter.id)]["Total"] = len(users[str(invite.inviter.id)]["Invited_Players"])
        except:
            pass
        for i in await member.guild.invites():
            if i.inviter == member:
                if users[str(user.id)]["Invites"] < i.uses:
                    users[str(user.id)]["Total"] = 0
                    users[str(user.id)]["Invites"] = 0
                    users[str(user.id)]["Leaves"] = 0
                    users[str(user.id)]["Invited_Players"] = []

                    with open("./cogs/json/invites.json", "w") as f:
                        json.dump(users, f, indent=4)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logs = self.client.get_channel(int(self.logs_channel))
        try:
            guild = self.client.get_guild(779319110885965844)
            for members in guild.members:

                await self.open_account(members)
                user = members
                users = await self.get_profile_data()

                if users[str(user.id)]["Invited_Players"].__contains__(str(member.id)):
                    users[str(user.id)]["Leaves"] += 1
                    users[str(user.id)]["Invited_Players"].remove(str(member.id))
                    users[str(user.id)]["Total"] = len(users[str(user.id)]["Invited_Players"])

                    with open("./cogs/json/invites.json", "w") as f:
                        json.dump(users, f, indent=4)
        except:
            pass

def setup(client):
    client.add_cog(Invite_tracker(client))