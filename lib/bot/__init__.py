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
        if datetime.date.today() == datetime.date(year=2022, month=4,day=29):
            await self.stdout.send("<@&884264858491691111> **Saint Catherine of Siena**\n\n**Saint of the Day for April 29 (March 25, 1347 – April 29, 1380)**\n\n__Saint Catherine of Siena’s Story__\nThe value Catherine makes central in her short life and which sounds clearly and consistently through her experience is complete surrender to Christ. What is most impressive about her is that she learns to view her surrender to her Lord as a goal to be reached through time. She was the 23rd child of Jacopo and Lapa Benincasa and grew up as an intelligent, cheerful, and intensely religious person. Catherine disappointed her mother by cutting off her hair as a protest against being overly encouraged to improve her appearance in order to attract a husband. Her father ordered her to be left in peace, and she was given a room of her own for prayer and meditation. She entered the Dominican Third Order at 18 and spent the next three years in seclusion, prayer, and austerity. Gradually, a group of followers gathered around her—men and women, priests and religious. An active public apostolate grew out of her contemplative life. Her letters, mostly for spiritual instruction and encouragement of her followers, began to take more and more note of public affairs. Opposition and slander resulted from her mixing fearlessly with the world and speaking with the candor and authority of one completely committed to Christ. She was cleared of all charges at the Dominican General Chapter of 1374. Her public influence reached great heights because of her evident holiness, her membership in the Dominican Third Order, and the deep impression she made on the pope. She worked tirelessly for the crusade against the Turks and for peace between Florence and the pope.")
            await self.stdout.send("In 1378, the Great Schism began, splitting the allegiance of Christendom between two, then three, popes and putting even saints on opposing sides. Catherine spent the last two years of her life in Rome, in prayer and pleading on behalf of the cause of Pope Urban VI and the unity of the Church. She offered herself as a victim for the Church in its agony. She died surrounded by her “children” and was canonized in 1461. Catherine ranks high among the mystics and spiritual writers of the Church. In 1939, she and Francis of Assisi were declared co-patrons of Italy. Pope Paul VI named her and Teresa of Avila doctors of the Church in 1970. Her spiritual testament is found in The Dialogue. \n__Reflection__\nThough she lived her life in a faith experience and spirituality far different from that of our own time, Catherine of Siena stands as a companion with us on the Christian journey in her undivided effort to invite the Lord to take flesh in her own life. Events which might make us wince or chuckle or even yawn fill her biographies: a mystical experience at six, childhood betrothal to Christ, stories of harsh asceticism, her frequent ecstatic visions. Still, Catherine lived in an age which did not know the rapid change of 21st-century mobile America. The value of her life for us today lies in her recognition of holiness as a goal to be sought over the course of a lifetime.\n__Saint Catherine of Siena is a Patron Saint of:__\nEurope\nFire Prevention\nItaly\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/painting-of-saint-catherine-of-siena.jpg?itok=wvJuhoBd")

        elif datetime.date.today() == datetime.date(year=2022, month=4,day=30):
            await self.stdout.send("<@&884264858491691111> **Saint Pius V**\n\n**Saint of the Day for April 30 (January 17, 1504 – May 1, 1572)**\n\n__Saint Pius V’s Story__\nThis is the pope whose job it was to implement the historic Council of Trent. If we think popes had difficulties in implementing Vatican Council II, Pius V had even greater problems after Trent four centuries earlier. During his papacy (1566-1572), Pius V was faced with the almost overwhelming responsibility of getting a shattered and scattered Church back on its feet. The family of God had been shaken by corruption, by the Reformation, by the constant threat of Turkish invasion, and by the bloody bickering of the young nation-states. In 1545, a previous pope convened the Council of Trent in an attempt to deal with all these pressing problems. Off and on over 18 years, the Fathers of the Church discussed, condemned, affirmed, and decided upon a course of action. The Council closed in 1563. Pius V was elected in 1566 and charged with the task of implementing the sweeping reforms called for by the Council. He ordered the founding of seminaries for the proper training of priests. He published a new missal, a new breviary, a new catechism, and established the Confraternity of Christian Doctrine classes for the young. Pius zealously enforced legislation against abuses in the Church. He patiently served the sick and the poor by building hospitals, providing food for the hungry, and giving money customarily used for the papal banquets to poor Roman converts. His decision to keep wearing his Dominican habit led to the custom–to this day–of the pope wearing a white cassock.")
            await self.stdout.send("In striving to reform both Church and state, Pius encountered vehement opposition from England’s Queen Elizabeth and the Roman Emperor Maximilian II. Problems in France and in the Netherlands also hindered Pius’s hopes for a Europe united against the Turks. Only at the last minute was he able to organize a fleet which won a decisive victory in the Gulf of Lepanto, off Greece, on October 7, 1571. Pius’ ceaseless papal quest for a renewal of the Church was grounded in his personal life as a Dominican friar. He spent long hours with his God in prayer, fasted rigorously, deprived himself of many customary papal luxuries, and faithfully observed the spirit of the Dominican Rule that he had professed.\n__Reflection__\nIn their personal lives and in their actions as popes, Saint Pius V and Saint Paul VI both led the family of God in the process of interiorizing and implementing the new birth called for by the Spirit in major Councils. With zeal and patience, Pius and Paul pursued the changes urged by the Council Fathers. Like Pius and Paul, we too are called to constant change of heart and life.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/portrait-of-pope-saint-pius-V.jpg?itok=OJNvdvZ9")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=1):
            await self.stdout.send("<@&884264858491691111> **Saint Joseph the Worker**\n\n**Saint of the Day for May 1**\n\n__The Story of Saint Joseph the Worker__\nTo foster deep devotion to Saint Joseph among Catholics, and in response to the “May Day” celebrations for workers sponsored by Communists, Pope Pius XII instituted the feast of Saint Joseph the Worker in 1955. This feast extends the long relationship between Joseph and the cause of workers in both Catholic faith and devotion. Beginning in the Book of Genesis, the dignity of human work has long been celebrated as a participation in the creative work of God. By work, humankind both fulfills the command found in Genesis to care for the earth (Gn 2:15) and to be productive in their labors. Saint Joseph, the carpenter and foster father of Jesus, is but one example of the holiness of human labor. Jesus, too, was a carpenter. He learned the trade from Saint Joseph and spent his early adult years working side-by-side in Joseph’s carpentry shop before leaving to pursue his ministry as preacher and healer. In his encyclical Laborem Exercens, Pope John Paul II stated: “the Church considers it her task always to call attention to the dignity and rights of those who work, to condemn situations in which that dignity and those rights are violated, and to help to guide [social] changes so as to ensure authentic progress by man and society.” Saint Joseph is held up as a model of such work. Pius XII emphasized this when he said, “The spirit flows to you and to all men from the heart of the God-man, Savior of the world, but certainly, no worker was ever more completely and profoundly penetrated by it than the foster father of Jesus, who lived with Him in closest intimacy and community of family life and work.”")
            await self.stdout.send("\n__Reflection__\nTo capture the devotion to Saint Joseph within the Catholic liturgy, in 1870, Pope Pius IX declared Saint Joseph the patron of the universal Church. In 1955, Pope Pius XII added the feast of Saint Joseph the Worker. This silent saint, who was given the noble task of caring and watching over the Virgin Mary and Jesus, now cares for and watches over the Church and models for all the dignity of human work.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/painting-of-saint-joseph-the-worker-with-young-jesus.jpg?itok=GbTAYglV")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=2):
            await self.stdout.send("<@&884264858491691111> **Saint Athanasius**\n\n**Saint of the Day for May 2 (c. 296 – May 2, 373)**\n\n__Saint Athanasius’ Story__\nAthanasius led a tumultuous but dedicated life of service to the Church. He was the great champion of the faith against the widespread heresy of Arianism, the teaching by Arius that Jesus was not truly divine. The vigor of his writings earned him the title of doctor of the Church. Born of a Christian family in Alexandria, Egypt, and given a classical education, Athanasius became secretary to Alexander, the bishop of Alexandria, entered the priesthood and was eventually named bishop himself. His predecessor, Alexander, had been an outspoken critic of a new movement growing in the East—Arianism. When Athanasius assumed his role as bishop of Alexandria, he continued the fight against Arianism. At first, it seemed that the battle would be easily won and that Arianism would be condemned. Such, however, did not prove to be the case. The Council of Tyre was called and for several reasons that are still unclear, the Emperor Constantine exiled Athanasius to northern Gaul. This was to be the first in a series of travels and exiles reminiscent of the life of Saint Paul. After Constantine died, his son restored Athanasius as bishop. This lasted only a year, however, for he was deposed once again by a coalition of Arian bishops. Athanasius took his case to Rome, and Pope Julius I called a synod to review the case and other related matters.")
            await self.stdout.send("Five times Athanasius was exiled for his defense of the doctrine of Christ’s divinity. During one period of his life, he enjoyed 10 years of relative peace—reading, writing, and promoting the Christian life along the lines of the monastic ideal to which he was greatly devoted. His dogmatic and historical writings are almost all polemic, directed against every aspect of Arianism. Among his ascetical writings, his Life of St. Anthony achieved astonishing popularity and contributed greatly to the establishment of monastic life throughout the Western Christian world.\n__Reflection__\nAthanasius suffered many trials while he was bishop of Alexandria. He was given the grace to remain strong against what probably seemed at times to be insurmountable opposition. Athanasius lived his office as bishop completely. He defended the true faith for his flock, regardless of the cost to himself. In today’s world we are experiencing this same call to remain true to our faith, no matter what.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/painting-of-saint-athanasius.jpg?itok=e5g1IXQ3")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=3):
            await self.stdout.send("<@&884264858491691111> **Saints Philip and James**\n\n**Saints of the Day for May 3**\n\n__Saints Philip and James’ Story__\nJames, Son of Alphaeus: We know nothing of this man except his name, and, of course, the fact that Jesus chose him to be one of the 12 pillars of the New Israel, his Church. He is not the James of Acts, son of Clopas, “brother” of Jesus and later bishop of Jerusalem and the traditional author of the Letter of James. James, son of Alphaeus, is also known as James the Lesser to avoid confusing him with James the son of Zebedee, also an apostle and known as James the Greater. Philip: Philip came from the same town as Peter and Andrew, Bethsaida in Galilee. Jesus called him directly, whereupon he sought out Nathanael and told him of the “one about whom Moses wrote” (Jn 1:45). Like the other apostles, Philip took a long time coming to realize who Jesus was. On one occasion, when Jesus saw the great multitude following him and wanted to give them food, he asked Philip where they should buy bread for the people to eat. Saint John comments, “[Jesus] said this to test him, because he himself knew what he was going to do” (Jn 6:6). Philip answered, “Two hundred days’ wages worth of food would not be enough for each of them to have a little [bit]” (Jn 6:7). John’s story is not a put-down of Philip. It was simply necessary for these men who were to be the foundation stones of the Church to see the clear distinction between humanity’s total helplessness apart from God and the human ability to be a bearer of divine power by God’s gift.")
            await self.stdout.send("On another occasion, we can almost hear the exasperation in Jesus’s voice. After Thomas had complained that they did not know where Jesus was going, Jesus said, “I am the way. If you know me, then you will also know my Father. From now on you do know him and have seen him” (Jn 14:6a, 7). Then Philip said, “Master, show us the Father, and that will be enough for us” (Jn 14:8). Enough! Jesus answered, “Have I been with you for so long a time and you still do not know me, Philip? Whoever has seen me has seen the Father” (Jn 14:9a). Possibly because Philip bore a Greek name or because he was thought to be close to Jesus, some gentile proselytes came to him and asked him to introduce them to Jesus. Philip went to Andrew, and Andrew went to Jesus. Jesus’s reply in John’s Gospel is indirect; Jesus says that now his “hour” has come, that in a short time he will give his life for Jew and gentile alike.\n__Reflection__\nAs in the case of the other apostles, we see in James and Philip human men who became foundation stones of the Church, and we are reminded again that holiness and its consequent apostolate are entirely the gift of God, not a matter of human achieving. All power is God’s power, even the power of human freedom to accept his gifts. “You will be clothed with power from on high,” Jesus told Philip and the others. Their first commission had been to expel unclean spirits, heal diseases, announce the kingdom. They learned, gradually, that these externals were sacraments of an even greater miracle inside their persons—the divine power to love like God.\n__Saints Philip and James are the Patron Saints of:__\nUruguay\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/painting-of-saints-philip-and-james.jpg?itok=d8WDooGj")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=4):
            await self.stdout.send("<@&884264858491691111> **Blessed Michael Giedroyc**\n\n**Saint of the Day for May 4 (c. 1425 – May 4, 1485)**\n\n__Blessed Michael Giedroyc’s Story__\nA life of physical pain and mental torment didn’t prevent Michael Giedroyc from achieving holiness. Born near Vilnius, Lithuania, Michael suffered from physical and permanent handicaps from birth. He was a dwarf who had the use of only one foot. Because of his delicate physical condition, his formal education was frequently interrupted. But over time, Michael showed special skills at metalwork. Working with bronze and silver, he created sacred vessels, including chalices. He traveled to Kraków, Poland, where he joined the Augustinians. He received permission to live the life of a hermit in a cell adjoining the monastery. There Michael spent his days in prayer, fasted and abstained from all meat and lived to an old age. Though he knew the meaning of suffering throughout his years, his rich spiritual life brought him consolation. Michael’s long life ended in 1485 in Kraków. Five hundred years later, Pope John Paul II visited the city and spoke to the faculty of the Pontifical Academy of Theology. The 15th century in Kraków, the pope said, was “the century of saints.” Among those he cited was Blessed Michael Giedroyc.")
            await self.stdout.send("\n__Reflection__\nMany people today face a life of suffering and discrimination due to physical handicaps. Let’s ask Blessed Michael Giedroyc to pray for them that their situation might be addressed by society at large.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/painting-of-blessed-michael-giedroyc.jpg?itok=PDEHcjCe")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=5):
            await self.stdout.send("<@&884264858491691111> **Saint Hilary of Arles**\n\n**Saint of the Day for May 5 (c. 401 – May 5, 449)**\n\n__Saint Hilary of Arles’ Story__\nIt’s been said that youth is wasted on the young. In some ways, that was true for today’s saint. Born in France in the early fifth century, Hilary came from an aristocratic family. In the course of his education he encountered his relative, Honoratus, who encouraged the young man to join him in the monastic life. Hilary did so. He continued to follow in the footsteps of Honoratus as bishop. Hilary was only 29 when he was chosen bishop of Arles. The new, youthful bishop undertook the role with confidence. He did manual labor to earn money for the poor. He sold sacred vessels to ransom captives. He became a magnificent orator. He traveled everywhere on foot, always wearing simple clothing. That was the bright side. Hilary encountered difficulty in his relationships with other bishops over whom he had some jurisdiction. He unilaterally deposed one bishop. He selected another bishop to replace one who was very ill–but, to complicate matters, did not die! Pope Saint Leo the Great kept Hilary a bishop but stripped him of some of his powers. Hilary died at 49. He was a man of talent and piety who in due time, had learned how to be a bishop.")
            await self.stdout.send("\n__Reflection__\nSaint Hilary teaches us to respect authority even if found in a young person. Age is not the issue: prudence and wisdom are.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/saint-hilary-of-arles.jpg?itok=-E3_uIMa")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=6):
            await self.stdout.send("<@&884264858491691111> **Saints Marian and James**\n\n**Saints of the Day for May 6 (d. May 6, 259)**\n\n__Saints Marian and James’s Story__\nSaint Marian, an ordained lector, and Saint James, a deacon, were martyred during the persecution of Valerian around the year 259. Few other facts are known about them. It seems that while they were in prison, each had a vision regarding his martyrdom. They drew courage from these apparitions and were able to courageously face death. They were joined in their deaths by other Christians.\n__Reflection__\nThe old saying that the more things change the more they stay the same may apply to today’s celebration. Two faithful people facing the hardships of life during persecution in the third century may have a lot in common with those facing persecution for their faith today.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/christian-martrys-in-the-colosseum.jpg?itok=CIpU1Aog")

        elif datetime.date.today() == datetime.date(year=2022, month=5,day=7):
            await self.stdout.send("<@&884264858491691111> **Saint Rose Venerini**\n\n**Saint of the Day for May 7 (February 9, 1656 – May 7, 1728)**\n\n__Saint Rose Venerini’s Story__\nRose was born at Viterbo in Italy, the daughter of a doctor. Following the death of her fiancé she entered a convent, but soon returned home to care for her newly widowed mother. Meanwhile, Rose invited the women of the neighborhood to recite the rosary in her home, forming a sort of sodality with them. As she looked to her future under the spiritual guidance of a Jesuit priest, Rose became convinced that she was called to become a teacher in the world rather than a contemplative nun in a convent. Clearly, she made the right choice: She was a born teacher, and the free school for girls she opened in 1685 was well received. Soon the cardinal invited her to oversee the training of teachers and the administration of schools in his diocese of Montefiascone. As Rose’s reputation grew, she was called upon to organize schools in many parts of Italy, including Rome. Her disposition was right for the task as well, for Rose often met considerable opposition but was never deterred. She died in Rome in 1728, where a number of miracles were attributed to her. She was beatified in 1952 and canonized in 2006. The sodality, or group of women she had invited to prayer, was ultimately given the rank of a religious congregation. Today, the so-called Venerini Sisters can be found in the United States and elsewhere, working among Italian immigrants.\n__Reflection__\nWhatever state of life God calls us to, we bring with us an assortment of experiences, interests and gifts—however small they seem to us. Rose’s life stands as a reminder that all we are is meant to be put to service wherever we find ourselves.\nhttps://www.franciscanmedia.org/sites/default/files/styles/blog_image/public/2022-03/statue-of-saint-rose-venerini.jpg?itok=Mwac4iUX")

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