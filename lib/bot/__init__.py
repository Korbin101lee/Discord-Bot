from asyncio import sleep
from datetime import datetime
from glob import glob
from pathlib import Path

from discord.ext.commands import when_mentioned_or, command, has_permissions

from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from discord import Embed, File, DMChannel
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Context
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from apscheduler.triggers.cron import CronTrigger

from ..db import db




OWNER_IDS = [830576756002914394]
#COGS = [Path.split("\\")[-1][:-3] for Path in glob("./lib/cogs/*.py")]
#COGS = [p.stem for p in Path(".").glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

#ODMxOTY5NzE0MDAyNzIyODE2.YHc-LQ.msEMnZmXuLxgEkwbh2tunzqjJwQ
TOKEN_TWO = "ODMxOTY5NzE0MDAyNzIyODE2.YHc-LQ.msEMnZmXuLxgEkwbh2tunzqjJwQ"
#Pro-Life client ID: #ODMxOTY5NzE0MDAyNzIyODE2.YHc-LQ.msEMnZmXuLxgEkwbh2tunzqjJwQ
#Bot-Testing client ID: ODg0MDkxNTYwOTgyMTEwMzA4.YTTcbQ.IdZJiKibnD0l7j6b8wbmvRzGHDc
GUILD_ID = 725187403253547040
#Pro-Life server ID: 808447993891389465
#Bot-Testing Server ID: 827970047297323019
STD_OUT = 727758880238469190
#Pro-Life channel ID: 808447994928037890
#Bot-Testing channel ID: 827970047297323022


def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    
    return when_mentioned_or(prefix)(bot, message)










class Bot(BotBase):
    def __init__(self):
        self.ready = False
        #self.cogs_ready = Ready()
        
        self.guild = None
        self.shceduler = AsyncIOScheduler()

        db.autosave(self.shceduler)
        self._cogs = [p.stem for p in Path(".").glob("./lib/cogs/*.py")]
        super().__init__(command_prefix=get_prefix, case_insensitive=True, owner_ids=OWNER_IDS,intents=Intents.all())



        

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:

            if not self.ready:
                await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

            else:
                await self.invoke(ctx)

    """def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")

        print("setup complete")"""

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in self._cogs])

    def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"Loaded `{cog}` cog.")

        print("Setup complete.")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

       # with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
          #  self.TOKEN = tf.read()
        
        print("running bot...")
        super().run(TOKEN_TWO, reconnect=True)

    async def rules_reminder(self):
        await self.stdout.send("Remember to adhere to the rules! ")


    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt")
        await self.shutdown()

    async def on_connect(self):
        print(f"Connected to Discord(latency: {self.latency*1000} ms).")

    async def on_resume(self):
        print("Bost resumed.")

    async def on_disconnected(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        #await self.stdout.send("An error occured.")
        raise

    

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} secs.")

        elif hasattr(exc, "original"):
            # if isinstance(exc.original, HTTPException):
            # 	await ctx.send("Unable to send message.")

            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permission to do that.")

            else:
                raise exc.original

        else:
            raise exc


    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(GUILD_ID)
            self.stdout = self.get_channel(STD_OUT)
            #self.shceduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.shceduler.start()


            #while not self.cogs_ready.all_ready():
            #    await sleep(0.5)
            #await self.stdout.send("Now online!")
            self.ready = True
            print(" bot ready")
            
        else:
            print("bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            if isinstance(message.channel, DMChannel):
                #if len(message.content) < 50:
                    #await message.channel.send("Your message should be at least 50 characters in length.")

                #else:
                member = self.guild.get_member(message.author.id)
                embed = Embed(title="Modmail",
                              color=member.color,
                              timestamp = datetime.utcnow())

                embed.set_thumbnail(url=member.avatar_url)

                fields = [("Member", member.display_name, False),
                        ("Message", message.content, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                mod = bot.get_cog("Mod")
                await mod.log_channel.send(embed=embed)
                await message.channel.send("Message relayed to moderators.")

            else:
                await self.process_commands(message)
                



    

    


bot = Bot()