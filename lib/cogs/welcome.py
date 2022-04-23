from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command

from ..db import db



class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    #@Cog.listener()
    #async def on_ready(self):
        #if not self.bot.ready:
            #self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        print(f"{member.guild.id}")            
        #db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        if member.guild.id == 883145816158650449:
            await member.add_roles(member.guild.get_role(918220652639576154))
            await self.bot.get_channel(883145817576333344).send(f"**IF YOU RECEIVED A DM FROM ALTIDENTIFIER, PLEASE ANSWER THAT FIRST** \n\nHey {member.mention}, welcome to Pro-Life! Before you get access to the rest of the channels, we would like you to answer a few questions. Please post them below and wait for an admin to approve you, which will happen within 12 hours, depending on your timezone. Please read the <#883145817576333345> as well. \n\n**DO NOT PING ADMINS OR OWNERS!**\n\nQuestions:\n1-Are you Pro-Life?\n2-If yes to #1, what exceptions may you consider (life of the mother, rape, etc.)?\n3-Where did you learn of this server?\n4-Do you agree to the rules?\n\nHave a good time!")
        
        if member.guild.id == 918238657566085150:
            await member.add_roles(member.guild.get_role(945777954380714085))
            await self.bot.get_channel(964303161504448592).send(f"**IF YOU RECEIVED A DM FROM ALTIDENTIFIER, PLEASE ANSWER THAT FIRST** \n\nHey {member.mention}, welcome to Pro-Life! Before you get access to the rest of the channels, we would like you to answer a few questions. Please post them below and wait for an admin to approve you, which will happen within 12 hours, depending on your timezone. Please read the <#964303221977911356> as well. \n\n**DO NOT PING ADMINS OR OWNERS!**\n\nQuestions:\n1-Are you Pro-Life?\n2-If yes to #1, what exceptions may you consider (life of the mother, rape, etc.)?\n3-Where did you learn of this server?\n4-Do you agree to the rules?\n\nHave a good time!")



        #await member.edit(roles=[*member.roles, *[member.guild.get_role(id_) for id_ in (829881736875474974, 829881823634522112)]])

    @Cog.listener()
    async def on_member_remove(self, member):
        #db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
        pass


def setup(bot):
    bot.add_cog(Welcome(bot))