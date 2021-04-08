from asyncio import sleep
from datetime import datetime
from glob import glob
from pathlib import Path

from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Context
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from apscheduler.triggers.cron import CronTrigger

from ..db import db

PREFIX = "+"
OWNER_IDS = [805261413702041621]
#COGS = [Path.split("\\")[-1][:-3] for Path in glob("./lib/cogs/*.py")]
COGS = [p.stem for p in Path(".").glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

TOKEN_TWO = "ODI4NzUxMTM0MDcxNzE3ODg4.YGuIow.z94e6h-SVwdzQnjJFaOrGPkmWBo"
#ODI3OTg2MjE5NDU5MTQ5OTA1.YGjAQQ.B-kl3xS5NmIsIdQzTIHqUWRGWvM

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])



class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        
        self.guild = None
        self.shceduler = AsyncIOScheduler()

        db.autosave(self.shceduler)
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS,intents=Intents.all())

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

        else:
            await ctx.send("I'm not ready to recieve commands. Please wait a few seconds.")

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")

        print("setup complete")

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

    async def on_connect(self):
        print(" bot connected")

    async def on_disconnected(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.stdout.send("An error occured.")
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
            self.guild = self.get_guild(808447993891389465)
            self.stdout = self.get_channel(808447994928037890)
            self.shceduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.shceduler.start()


            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            await self.stdout.send("Now online!")
            self.ready = True
            print(" bot ready")
            
        else:
            print("bot reconnected")

    async def on_message(self, message):
        
        if not message.author.bot:
            await self.process_commands(message)

    


bot = Bot()