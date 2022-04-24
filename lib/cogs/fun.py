from random import choice, randint
from typing import Optional

from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"])
    @cooldown(1, 2, BucketType.member)
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'hiya'))} {ctx.author.mention}!")

    @command(name="Robert")
    async def say_hello(self, ctx):
        await ctx.send(f"please be nice <:PrayTheTayAway:883906727291027486>")

    @command(name="dice", aliases=["roll"])
    @cooldown(1, 2, BucketType.member)
    async def roll_dice(self, ctx, die_string: str):
	    dice, value = (int(term) for term in die_string.split("d"))

	    if dice <= 25:
	    	rolls = [randint(1, value) for i in range(dice)]

	    	await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

	    else:
	    	await ctx.send("I can't roll that many dice. Please try a lower number.")


    @command(name="slap", aliases=["hit"])
    @cooldown(1, 2, BucketType.member)
    async def slap_member(self, ctx, member:Member, *, reason:Optional[str] = "no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I can't find that member.")


    @command(name="echo", aliases=["say"])
    @cooldown(1, 2, BucketType.member)
    async def echo_message(self,ctx, *, message):
        await  ctx.message.delete()
        await ctx.send(message)

    @command(name="anime")
    @cooldown(1, 2, BucketType.member)
    async def animal_fact(self, ctx, anime: str):
        if (anime := anime.lower()) in ("wink", "pat", "hug"):
            image_url = f"https://some-random-api.ml/animu/{'pat' if anime == 'pat' else anime}"
            
            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None
            

                if image_link is not None:
                    embed.set_image(url=image_link)
                await ctx.send(embed=embed)


    @command(name="fact")
    @cooldown(1, 2, BucketType.member)
    async def animal_fact(self, ctx, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"
            
            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None
            
            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(title=f"{animal.title()} fact",
                                   description=data["fact"],
                                   color=ctx.author.color)
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            await ctx.send("No facts are avaliable for that animal.")


    
    @command(pass_context=True)
    async def Rules(self, ctx):
        embed= Embed(title="**Pro-Life**", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", color=0x00aaff)
        embed.set_author(name="Pro-Life", icon_url="https://cdn.discordapp.com/icons/808447993891389465/61f30606d380c58a51323eba3957d00f.webp?size=128")
        embed.add_field(name="**Rule 1: **", value="To be admitted into and remain in the server, you must be pro-life. ", inline=False)
        embed.add_field(name="**Rule 2: **", value="No harassment or bullying will be tolerated.", inline=False)
        embed.add_field(name="**Rule 3: **", value="No graphic or sexually explicit media (pictures, gifs, videos, no rhino shit gif)", inline=False)
        embed.add_field(name="**Rule 4: **", value="Use the text and voice channels for their proper, designated use.", inline=False)
        embed.add_field(name="**Rule 5: **", value="No spamming, this includes bot spam.", inline=False)
        embed.add_field(name="**Rule 6: **", value="No planning or participating in doxing or raids, no doxing is allowed.", inline=False)
        embed.add_field(name="**Rule 7: **", value="Slurs are not to be used in a derogatory way.", inline=False)
        embed.add_field(name="**Rule 8: **", value="Do not go into channels you aren't supposed to enter (example: entering the Christian channel knowing that you are an atheist and vice versa). The owners are obviously exempt from this rule.", inline=False)
        embed.add_field(name="**Rule 9: **", value="Impersonating another server member is not allowed.", inline=False)
        embed.add_field(name="**Rule 10: **", value="Do not block admins without permission from the owner.", inline=False)
        embed.add_field(name="**Rule 11: **", value="No advocating for self harm of any kind.", inline=False)
        embed.add_field(name="**Rule 12: **", value="No racism, anti-Semitism, or any kind of discrimination will be tolerated.", inline=False)
        embed.add_field(name="**Rule 13: **", value="Do not use the mass pings.", inline=False)
        embed.add_field(name="**Rule 14: **", value="Staff will deem whether a nickname is inappropriate or not.", inline=False)
        embed.add_field(name="**Rule 15: **", value="No trolling (We do not do a little trolling)", inline=False)
        embed.add_field(name="**Rule 16: **", value="Follow the Discord ToS and Community Guidelines", inline=False)
        embed.set_footer(text="Staff have full discretion to enforce the rules as they see fit.")
        await ctx.send(embed=embed)


    #@Cog.listener()
    #async def on_ready(self):
        #if not self.bot.ready:
            #self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))