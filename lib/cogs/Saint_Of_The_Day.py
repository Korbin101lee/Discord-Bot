from random import choice, randint
from typing import Optional

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown
import datetime
import schedule
import time


t = datetime.datetime.now()
date_time = t.strftime("%m/%d/%Y, %H:%M")

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot


    
    async def SaintOfTheDay(self, ctx):
        if (datetime.date(2022, 4, 24) == datetime.date(2022, 4, 24)):
            await ctx.get_channel(883360065422250048).send(f"<@&884274014388891678>	 **Saint Fidelis of Sigmaringen Saint of the Day for April 24 (1577 – April 24, 1622)**\n \n __Saint Fidelis of Sigmaringen’s Story__ \n If a poor man needed some clothing, Fidelis would often give the man the clothes right off his back. Complete generosity to others characterized this saint’s life. Born in 1577, Mark Rey became a lawyer who constantly upheld the causes of the poor and oppressed people. Nicknamed “the poor man’s lawyer,” Rey soon grew disgusted with the corruption and injustice he saw among his colleagues. He left his law career to become a priest, joining his brother George as a member of the Capuchin Order. Fidelis was his religious name. His wealth was divided between needy seminarians and the poor. As a follower of Saint Francis of Assisi, Fidelis continued his devotion to the weak and needy. During a severe epidemic in a city where he was guardian of a friary, Fidelis cared for and cured many sick soldiers. He was appointed head of a group of Capuchins sent to preach against the Calvinists and Zwinglians in Switzerland. Almost certain violence threatened. Those who observed the mission felt that success was more attributable to the prayer of Fidelis during the night than to his sermons and instructions. He was accused of opposing the peasants’ national aspirations for independence from Austria. While he was preaching at Seewis, to which he had gone against the advice of his friends, a gun was fired at him, but he escaped unharmed. A Protestant offered to shelter Fidelis, but he declined, saying his life was in God’s hands. On the road back, he was set upon by a group of armed men and killed. Fidelis was canonized in 1746. Fifteen years later he was recognized as a martyr. \n ")
            await ctx.get_channel(883360065422250048).send(f"__Reflection__ \n Fidelis’ constant prayer was that he be kept completely faithful to God and not give in to any lukewarmness or apathy. He was often heard to exclaim, “Woe to me if I should prove myself but a halfhearted soldier in the service of my thorn-crowned Captain.” His prayer against apathy, and his concern for the poor and weak make him a saint whose example is valuable today. The modern Church is calling us to follow the example of “the poor man’s lawyer” by sharing ourselves and our talents with those less fortunate and by working for justice in the world.")
        print("works")

        
    #@Cog.listener()
    #async def on_ready(self):
        #if not self.bot.ready:
            #self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))