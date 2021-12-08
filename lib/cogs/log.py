from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
import discord

class Log(Cog):
    def __init__(self,bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.log_channel = self.bot.get_channel(887417626324791316)
            #pro life log channel: 808563375944106074
            #testing bot log channel: 828785261449445486
            #self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = Embed(title="Username change",
                          color=after.color,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.name, False),
                      ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = Embed(title="Discriminator change",
                           color=after.color,
                            timestamp=datetime.utcnow())

            fields = [("Before", before.discriminator, False),
                      ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        if before.avatar_url != after.avatar_url:
            embed = Embed(title="Avatar change",
                            description="New image is below, old to the right.",
                            color=self.log_channel.guild.get_member(after.id).color,
                            timestamp=datetime.utcnow())
            
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = Embed(title="Nickname update",
                          color=after.color,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        """elif before.roles != after.roles:
            embed=Embed(title="", description=f"{before.mention} ** was given the ** {r.roles for r in after.roles} **role**",  color=0xdd2222, timestamp=datetime.utcnow())
            embed.set_author(name=f"{before.name}", icon_url="https://cdn.discordapp.com/avatars/828751134071717888/4d74c445b46ea32c77f88f241ba574c3.webp?size=1024")
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_footer(text=f"ID: {before.id}")
            await self.log_channel.send(embed=embed)"""


    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:
                embed=Embed(title="", description=f"**Message edited in** <#{before.channel.id}> [Jump to Message]({before.jump_url})",  color=0xdd2222, timestamp=datetime.utcnow())
                #embed.add_field(name=f"Message edited in ", value=f"<#{before.channel.id}>", inline=False)
                embed.set_author(name=f"{before.author}", icon_url="https://cdn.discordapp.com/avatars/828751134071717888/4d74c445b46ea32c77f88f241ba574c3.webp?size=1024")
                embed.set_thumbnail(url=before.author.avatar_url)
                embed.add_field(name="Before", value=f"{before.content}", inline=False)
                embed.add_field(name="After", value=f"{after.content}", inline=False)
                embed.set_footer(text=f"ID: {before.id}")
                await self.log_channel.send(embed=embed)

            

    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
                embed=Embed(title="", description=f"**Message sent by ** <@{message.author.id}> **deleted in** <#{message.channel.id}> {message.content}",  color=0xdd2222, timestamp=datetime.utcnow())
                #embed.add_field(name=None, value=f"{message.content}", inline=False)
                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_author(name=f"{message.author}", icon_url="https://cdn.discordapp.com/avatars/828751134071717888/4d74c445b46ea32c77f88f241ba574c3.webp?size=1024")
                embed.set_footer(text=f"Author:{message.author.id} | Message ID:{message.id}")
                await self.log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Log(bot))