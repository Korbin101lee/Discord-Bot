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
        embed.add_field(name="**Rule 1 - You MUST be Pro-Life:**", value="If you aren't, join this server: https://discord.gg/hgjFmKrARW", inline=False)
        embed.add_field(name="**Rule 2 - Toxicity/Respect:**", value="We do not mind friendly banter, but attacking or harassing anyone when they're clearly uncomfortable is unacceptable. It is up to the staff team's discretion on what is considered too excessive.", inline=False)
        embed.add_field(name="**Rule 3 - Innapropriate words:**", value="Do not use any form of Slurs, Profanity, Insults, NSFW language, Disrespectful language.", inline=False)
        embed.add_field(name="**Rule 4 - No Doxing:**", value="Do not post someone's private information without permission to do so from them.", inline=False)
        embed.add_field(name="**Rule 5 - Spam/Pings:**", value="Do not spam pings, messages, or images. Do not ghost ping. Do not ping Mods without a good reason.", inline=False)
        embed.add_field(name="**Rule 6 - appropriate channels:**", value="Please use the appropriate channels for this server. Please keep debating out of general.", inline=False)
        embed.add_field(name="**Rule 7 - Do not post NSFW/Gore:**", value="Do not have or post sexually suggestive, potential fetishes or gore containing messages, images, videos, links, profile pictures, statuses, or names. It is up to the staff team's discretion on what is considered to explicit/excessive.", inline=False)
        embed.add_field(name="**Rule 8 - Username:**", value="If your username is not, please create a nickname that is legible, sensible, and can be pinged easily. It is up to staff team's discretion on what is considered sensible and the staff team may change your username for you.", inline=False)
        embed.add_field(name="**Rule 9 - Staff/Pro-Life Bot Contact:**", value="Contact a member of staff or Pro-Life discord bot if you witness a rule violation.", inline=False)
        embed.add_field(name="**Rule 10 - Music bot:**", value="Please do not create a long queue with The Music Bot. Let other people play songs as well. Don't skip other people's songs. And please Do not play bad, inappropriate songs on The Music Bot.", inline=False)
        embed.add_field(name="**Rule 11 - Advertising/Link:**", value="Do not do any form of DM Advertising without permission, do not send links into channels you can DM a staff member if you wanna partner with the server. This will result in a warning, mute, or ban depending on the severity.", inline=False)
        embed.add_field(name="**Rule 12 - Moderation/Staff:**", value="Do not disrespect staff members for a moderation decision. Comply and if you reall think what happened was unjust file a complaint with one of the owners.", inline=False)
        embed.add_field(name="**Rule 13 - Server/Community:**", value="Any action undertaken by a staff member of this server that can be viewed as hostile/inflammatory to another server is neither encouraged nor allowed.", inline=False)
        embed.add_field(name="**Rule 14 - Roles:**", value="Do not take the wrong discord Roles and gain access to channels you are not allowed to be in.", inline=False)
        embed.add_field(name="**Rule 15 - Lying:**", value="Do not lie to anyone please be truthful on your verification and on your roles.", inline=False)
        embed.add_field(name="**Rule 16 - Discord TOS:**", value="Do not violate the Discord Terms of Service. (https://discord.com/terms)", inline=False)
        embed.set_footer(text="Pro-Life Bot was made by the Pro-Life development team, please DM the bot for more information")
        await ctx.send(embed=embed)


    #@Cog.listener()
    #async def on_ready(self):
        #if not self.bot.ready:
            #self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))