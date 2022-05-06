from asyncio import sleep
import asyncio
from datetime import datetime
from glob import glob
from pathlib import Path
import json, random, datetime

from discord.ext.commands import when_mentioned_or, command, has_permissions

from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from discord import Embed, File, DMChannel
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Context
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from apscheduler.triggers.cron import CronTrigger
from discord.ext import tasks, commands

from ..db import db
import datetime

time = datetime.datetime.now()
date_time = time.strftime("%m/%d/%Y, %H:%M")



OWNER_IDS = [830576756002914394]
#COGS = [Path.split("\\")[-1][:-3] for Path in glob("./lib/cogs/*.py")]
#COGS = [p.stem for p in Path(".").glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

#ODMxOTY5NzE0MDAyNzIyODE2.YHc-LQ.msEMnZmXuLxgEkwbh2tunzqjJwQ
TOKEN_TWO = "ODMxOTY5NzE0MDAyNzIyODE2.YHc-LQ.msEMnZmXuLxgEkwbh2tunzqjJwQ"
#Pro-Life 2 Client ID #OTI3Mjg1MTM0OTY3ODY1MzY1.YdH_lA.j8_UEMqqMg7TPNlxLVJzZcjPssc
#Pro-Life client ID: #ODMxOTY5NzE0MDAyNzIyODE2.YHc-LQ.msEMnZmXuLxgEkwbh2tunzqjJwQ
#Bot-Testing client ID: ODg0MDkxNTYwOTgyMTEwMzA4.YTTcbQ.IdZJiKibnD0l7j6b8wbmvRzGHDc
GUILD_ID = 719251528556478524

#Pro-Life server ID: 808447993891389465
#Bot-Testing Server ID: 827970047297323019
STD_OUT = 884113611444854925
#Pro-Life channel ID: 808447994928037890
#Bot-Testing channel ID: 827970047297323022
import discord

bot2 = discord.Client()#




def get_prefix(bot, message):
	db.execute("INSERT OR IGNORE INTO guilds(GuildID) VALUES(?)", message.guild.id)
	prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    
	return when_mentioned_or(prefix)(bot, message)





#song_url = field("SELECT Track_Url FROM music_player")

prefix = db.field("SELECT Prefix FROM guilds")

client = commands.Bot(prefix)








class Bot(BotBase):
    def __init__(self):
        self.ready = False
        #self.cogs_ready = Ready()
        
        self.guild = None
        #self.shceduler = AsyncIOScheduler()
        
        #db.autosave(self.shceduler)
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
    
    @tasks.loop(hours = 24) # repeat after every 24 hours
    async def send_message(self):

        if datetime.date.today() == datetime.date(year=2022, month=5,day=6):
            await self.stdout.send("<@&884264858491691111> **Saints Marian and James**\n\n**Saints of the Day for May 6 (d. May 6, 259)**\n\n__Saints Marian and James’s Story__\nSaint Marian, an ordained lector, and Saint James, a deacon, were martyred during the persecution of Valerian around the year 259. Few other facts are known about them. It seems that while they were in prison, each had a vision regarding his martyrdom. They drew courage from these apparitions and were able to courageously face death. They were joined in their deaths by other Christians.\n__Reflection__\nThe old saying that the more things change the more they stay the same may apply to today’s celebration. Two faithful people facing the hardships of life during persecution in the third century may have a lot in common with those facing persecution for their faith today.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/christian-martrys-in-the-colosseum.jpg?itok=CIpU1Aog")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=7):
            await self.stdout.send("<@&884264858491691111> **Saint Rose Venerini**\n\n**Saint of the Day for May 7 (February 9, 1656 – May 7, 1728)**\n\n__Saint Rose Venerini’s Story__\nRose was born at Viterbo in Italy, the daughter of a doctor. Following the death of her fiancé she entered a convent, but soon returned home to care for her newly widowed mother. Meanwhile, Rose invited the women of the neighborhood to recite the rosary in her home, forming a sort of sodality with them. As she looked to her future under the spiritual guidance of a Jesuit priest, Rose became convinced that she was called to become a teacher in the world rather than a contemplative nun in a convent. Clearly, she made the right choice: She was a born teacher, and the free school for girls she opened in 1685 was well received. Soon the cardinal invited her to oversee the training of teachers and the administration of schools in his diocese of Montefiascone. As Rose’s reputation grew, she was called upon to organize schools in many parts of Italy, including Rome. Her disposition was right for the task as well, for Rose often met considerable opposition but was never deterred. She died in Rome in 1728, where a number of miracles were attributed to her. She was beatified in 1952 and canonized in 2006. The sodality, or group of women she had invited to prayer, was ultimately given the rank of a religious congregation. Today, the so-called Venerini Sisters can be found in the United States and elsewhere, working among Italian immigrants.\n__Reflection__\nWhatever state of life God calls us to, we bring with us an assortment of experiences, interests and gifts—however small they seem to us. Rose’s life stands as a reminder that all we are is meant to be put to service wherever we find ourselves.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/statue-of-saint-rose-venerini.jpg?itok=Mwac4iUX")
 
        elif datetime.date.today() == datetime.date(year=2022, month=5,day=8):
            await self.stdout.send("<@&884264858491691111> **Saint Peter of Tarentaise**\n\n**Saint of the Day for May 8 (1102 – 1174)**\n\n__Saint Peter of Tarentaise’s Story__\nThere are two men named Saint Peter of Tarentaise who lived one century apart. The man we honor today is the elder Peter, born in France in the early part of the 12th century. The other man with the same name became Pope Innocent the Fifth. The Peter we’re focusing on today became a Cistercian monk and eventually served as abbot. In 1142, he was named archbishop of Tarentaise, replacing a bishop who had been deposed because of corruption. Peter tackled his new assignment with vigor. He brought reform into his diocese, replaced lax clergy, and reached out to the poor. He visited all parts of his mountainous diocese on a regular basis. After about a decade as bishop, Peter “disappeared” for a year and lived quietly as a lay brother at an abbey in Switzerland. When he was found out, the reluctant bishop was persuaded to return to his post. He again focused many of his energies on the poor. Peter died in 1174 on his way home from an unsuccessful papal assignment to reconcile the kings of France and England. His liturgical feast is celebrated on September 14. \n__Reflection__\nWe probably know a lot of people who would welcome the chance to receive some honor or honorary position. They relish the thought of the glamour and glory. But saints like Peter of Tarentaise remind us that humility and the avoidance of glory is the way of the Gospel.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/papal-bull-of-pope-alexander-III.jpg?itok=KmoPfsWD")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=9):
            await self.stdout.send("<@&884264858491691111> **Saint John of Avila**\n\n**Saint of the Day for May 9 (c. 1500 – May 10, 1569)**\n\n__Saint John of Avila’s Story__\nBorn in the Castile region of Spain, John was sent at the age of 14 to the University of Salamanca to study law. He later moved to Alcala, where he studied philosophy and theology before his ordination as a diocesan priest. After John’s parents died and left him as their sole heir to a considerable fortune, he distributed his money to the poor. In 1527, he traveled to Seville, hoping to become a missionary in Mexico. The archbishop of that city persuaded him to stay and spread the faith in Andalusia. During nine years of work there, he developed a reputation as an engaging preacher, a perceptive spiritual director, and a wise confessor. Because John was not afraid to denounce vice in high places, he was investigated by the Inquisition but was cleared in 1533. He later worked in Cordoba and then in Granada, where he organized the University of Baeza, the first of several colleges run by diocesan priests who dedicated themselves to teaching and giving spiritual direction to young people. He was friends with Saints Francis Borgia, Ignatius of Loyola, John of God, John of the Cross, Peter of Alcantara, and Teresa of Avila. John of Avila worked closely with members of the Society of Jesus and helped their growth within Spain and its colonies. John’s mystical writings have been translated into several languages. He was beatified in 1894, canonized in 1970, and declared a doctor of the Church on October 7, 2012. St. John of Avila's liturgical feast is celebrated on May 10.")
            await self.stdout.send("\n__Reflection__\nSaint John of Avila knew that the lives of Christians can contradict the Good News of Jesus Christ—for example thinking racism is OK—implicitly encouraging Christians to live their faith-halfheartedly, and causing obstacles to non-Christians who might accept Baptism. In 16th-century Spain, those who advocated reforming the Church were often suspected of heresy. Saint John of Avila held his ground and was eventually recognized as a very reliable teacher of the Christian faith.\n__John of Avila is the Patron Saint of:__\nAndalusia, Spain\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/portrait-of-saint-john-of-avila.jpg?itok=J5Cqtz8g")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=10):
            await self.stdout.send("<@&884264858491691111> **Saint Damien de Veuster of Moloka’i**\n\n**Saint of the Day for May 10 (January 3, 1840 – April 15, 1889)**\n\n__Saint Damien de Veuster of Moloka’i’s Story__\nWhen Joseph de Veuster was born in Tremelo, Belgium, in 1840, few people in Europe had any firsthand knowledge of leprosy, Hansen’s disease. By the time he died at the age of 49, people all over the world knew about this disease because of him. They knew that human compassion could soften the ravages of this disease. Forced to quit school at age 13 to work on the family farm, Joseph entered the Congregation of the Sacred Hearts of Jesus and Mary six years later, taking the name of a fourth-century physician and martyr. When his brother Pamphile, a priest in the same congregation, fell ill and was unable to go to the Hawaiian Islands as assigned, Damien quickly volunteered in his place. In May 1864, two months after arriving in his new mission, Damien was ordained a priest in Honolulu and assigned to the island of Hawaii. In 1873, he went to the Hawaiian government’s leper colony on the island of Moloka’i, set up seven years earlier. Part of a team of four chaplains taking that assignment for three months each year, Damien soon volunteered to remain permanently, caring for the people’s physical, medical, and spiritual needs. In time, he became their most effective advocate to obtain promised government support. Soon the settlement had new houses and a new church, school and orphanage. Morale improved considerably. A few years later, he succeeded in getting the Franciscan Sisters of Syracuse, led by Mother Marianne Cope, to help staff this colony in Kalaupapa. Damien contracted Hansen’s disease and died of its complications. As requested, he was buried in Kalaupapa, but in 1936 the Belgian government succeeded in having his body moved to Belgium. Part of Damien’s body was returned to his beloved Hawaiian brothers and sisters after his beatification in 1995.")
            await self.stdout.send("When Hawaii became a state in 1959, it selected Damien as one of its two representatives in the Statuary Hall at the US Capitol. Damien was canonized by Pope Benedict XVI on October 11, 2009. \n__Reflection__\nSome people thought Damien was a hero for going to Moloka’i and others thought he was crazy. When a Protestant clergyman wrote that Damien was guilty of immoral behavior, Robert Louis Stevenson vigorously defended him in an “Open Letter to Dr. Hyde.”\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/saint-hilary-of-arles.jpg?itok=-E3_uIMa")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=11):
            await self.stdout.send("<@&884264858491691111> **Saint Ignatius of Laconi**\n\n**Saint of the Day for May 11 (December 17, 1701 – May 11, 1781)**\n\n__Saint Ignatius of Laconi’s Story__\nIgnatius is another sainted begging brother. He was the second of seven children of peasant parents in Sardinia. His path to the Franciscans was unusual. During a serious illness, Ignatius vowed to become a Capuchin if he recovered. He regained his health but ignored the promise. When he was 20, a riding accident prompted Ignatius to renew the pledge, which he acted on the second time. Ignatius’s reputation for self-denial and charity led to his appointment as the official beggar for the friars in Cagliari. He fulfilled that task for 40 years, despite being blind for the last two years. While on his rounds, Ignatius would instruct the children, visit the sick, and urge sinners to repent. The people of Cagliari were inspired by his kindness and his faithfulness to his work. Ignatius was canonized in 1951.\n__Reflection__\nWhy did the people of Cagliari support the friars? These followers of Francis worked hard but rarely at jobs that paid enough to live on. The life of Ignatius reminds us that everything God considers worthwhile does not have a high-paying salary attached to it.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/statue-of-saint-ignatius-of-laconi.jpg?itok=VVYs41Sf")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=12):
            await self.stdout.send("<@&884264858491691111> **Saint Leopold Mandic**\n\n**Saint of the Day for May 12 (May 12, 1866 – July 30, 1942)**\n\n__Saint Leopold Mandic’s story__\nWestern Christians who are working for greater dialogue with Orthodox Christians may be reaping the fruits of Father Leopold’s prayers. A native of Croatia, Leopold joined the Capuchin Franciscans and was ordained several years later in spite of several health problems. He could not speak loudly enough to preach publicly. For many years he also suffered from severe arthritis, poor eyesight, and a stomach ailment. For several years Leopold taught patrology, the study of the Church Fathers, to the clerics of his province, but he is best known for his work in the confessional, where he sometimes spent 13-15 hours a day. Several bishops sought out his spiritual advice. Leopold’s dream was to go to the Orthodox Christians and work for the reunion of Roman Catholicism and Orthodoxy. His health never permitted it. Leopold often renewed his vow to go to the Eastern Christians; the cause of unity was constantly in his prayers. At a time when Pope Pius XII said that the greatest sin of our time is “to have lost all sense of sin,” Leopold had a profound sense of sin and an even firmer sense of God’s grace awaiting human cooperation. Leopold, who lived most of his life in Padua, died on July 30, 1942, and was canonized in 1982. In the Roman liturgy his feast is celebrated on July 30.")
            await self.stdout.send("\n__Reflection__\nSaint Francis advised his followers to “pursue what they must desire above all things, to have the Spirit of the Lord and His holy manner of working” (Rule of 1223, Chapter 10)—words that Leopold lived out. When the Capuchin minister general wrote his friars on the occasion of Leopold’s beatification, he said that this friar’s life showed “the priority of that which is essential.”\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/statue-of-saint-leopold-mandic.jpg?itok=Le1FU5Fa")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=13):
            await self.stdout.send("<@&884264858491691111> **Our Lady of Fatima**\n\n**Saint of the Day for May 13**\n\n__The Story of Our Lady of Fatima__\nBetween May 13 and October 13, 1917, three Portuguese children–Francisco and Jacinta Marto and their cousin Lucia dos Santos–received apparitions of Our Lady at Cova da Iria near Fatima, a city 110 miles north of Lisbon. Mary asked the children to pray the rosary for world peace, for the end of World War I, for sinners, and for the conversion of Russia. Mary gave the children three secrets. Following the deaths of Francisco and Jacinta in 1919 and 1920 respectively, Lucia revealed the first secret in 1927. It concerned devotion to the Immaculate Heart of Mary. The second secret was a vision of hell. When Lucia grew up she became a Carmelite nun and died in 2005 at the age of 97. Pope John Paul II directed the Holy See’s Secretary of State to reveal the third secret in 2000; it spoke of a “bishop in white” who was shot by a group of soldiers who fired bullets and arrows into him. Many people linked this vision to the assassination attempt against Pope John Paul II in St. Peter’s Square on May 13, 1981. The feast of Our Lady of Fatima was approved by the local bishop in 1930; it was added to the Church’s worldwide calendar in 2002.")
            await self.stdout.send("\n__Reflection__\nThe message of Fatima is simple: Pray. Unfortunately, some people—not Sister Lucia—have distorted these revelations, making them into an apocalyptic event for which they are now the only reliable interpreters. They have, for example, claimed that Mary’s request that the world be consecrated to her has been ignored. Sister Lucia agreed that Pope John Paul II’s public consecration in St. Peter’s Square on March 25, 1984, fulfilled Mary’s request. The Congregation for the Doctrine of the Faith prepared a June 26, 2000, document explaining the “third secret.” Mary is perfectly honored when people generously imitate her response “Let it be done to me as you say” (Luke 1:38). Mary can never be seen as a rival to Jesus or to the Church’s teaching authority, as exercised by the college of bishops united with the bishop of Rome.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/our-lady-of-fatima.jpg?itok=d7H1h_kC")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=14):
            await self.stdout.send("<@&884264858491691111> **Saint Matthias**\n\n**Saint of the Day for May 14**\n\n__Saint Matthias’ Story__\nAccording to Acts 1:15-26, during the days after the Ascension Peter stood up in the midst of the brothers—about 120 of Jesus’ followers. Now that Judas had betrayed his ministry, it was necessary, Peter said, to fulfill the scriptural recommendation that another should take his office. “Therefore, it is necessary that one of the men who accompanied us the whole time the Lord Jesus came and went among us, beginning from the baptism of John until the day on which he was taken up from us, become with us a witness to his resurrection” (Acts 1:21-22). They nominated two men: Joseph Barsabbas and Matthias. They prayed and drew lots. The choice fell upon Matthias, who was added to the Eleven. Matthias is not mentioned by name anywhere else in the New Testament.\n__Reflection__\nWhat was the holiness of Matthias? Obviously, he was suited for apostleship by the experience of being with Jesus from his baptism to his ascension. He must also have been suited personally, or he would not have been nominated for so great a responsibility. Must we not remind ourselves that the fundamental holiness of Matthias was his receiving gladly the relationship with the Father offered him by Jesus and completed by the Holy Spirit? If the apostles are the foundations of our faith by their witness, they must also be reminders, if only implicitly, that holiness is entirely a matter of God’s giving, and it is offered to all, in the everyday circumstances of life. We receive, and even for this God supplies the power of freedom.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/icon-of-saint-matthias.jpg?itok=fCaEwfl4")


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
            #self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=0, minute=0, second=11))
            #self.shceduler.add_job(self.SaintOfTheDay, 'interval', seconds=10)
            #self.shceduler.start()
           # self.sched = AsyncIOScheduler()
           # self.sched.start()
           # self.sched.add_job(self.send_message(), CronTrigger(hour=23, minute=10, second=0)) #on 00:00

            self.send_message.start()
            #await self.send_message.start()

        
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