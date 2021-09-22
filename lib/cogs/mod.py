from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional
import json
import os
import discord
from pathlib import Path

from discord import Embed, Member, NotFound, Object
from discord.utils import find
from discord.ext.commands import Cog, Greedy, Converter
from discord.ext.commands import CheckFailure, BadArgument
from discord.ext.commands import command, has_permissions, bot_has_permissions
import re






  
# create a sample json
  
  
# Convert JSON to String
  
  





class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

        

    @command(name="kick")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_members(self, ctx, user: Member, *, reason: Optional[str] = "No reason provided."):
        if (ctx.guild.me.top_role.position > user.top_role.position 
            and not user.guild_permissions.administrator):
            await user.send(f"You got Kicked for: {reason} by <@{ctx.author.id}>")
            await user.kick(reason=reason)

            embed = Embed(title=f"User Kicked | {user}",
                        color=0xDD2222,
                        timestamp=datetime.utcnow())

            embed=discord.Embed(title=f"User Kicked | {user}", color=0xdd2222, timestamp=datetime.utcnow())
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="User", value=f"<@{user.id}>", inline=True)
            embed.add_field(name="Moderator", value=f"<@{ctx.author.id}>", inline=True)
            embed.add_field(name="Reason", value="reason", inline=True)
            embed.set_footer(text=f"ID: {user.id}")
            await self.log_channel.send(embed=embed)

        else:
            await ctx.send(f"{user.display_name} could not be kicked.")

        await ctx.send("Action complete.")


    @kick_members.error
    async def kick_members_error(self,ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Insufficient permissions to perform that task.")

    @command(name="verify")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def verify(self, ctx, member : Member):
        await member.remove_roles(member.guild.get_role(789324989027319838  ))
        await member.add_roles(member.guild.get_role(725211551069503508))
        await ctx.send(f"Welcome to the server {member.display_name} you can get roles in <#725193339028373586>")


    @command(name="ban")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_members(self, ctx, user: Member, *, reason: Optional[str] = "No reason provided."):
        if (ctx.guild.me.top_role.position > user.top_role.position 
            and not user.guild_permissions.administrator):
            await user.send(f"You got Banned for: {reason} by <@{ctx.author.id}>")
            await user.ban(reason=reason)

            embed = Embed(title=f"User Banned | {user}",
                        color=0xDD2222,
                        timestamp=datetime.utcnow())

            embed=discord.Embed(title=f"User Banned | {user}", color=0xdd2222, timestamp=datetime.utcnow())
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="User", value=f"<@{user.id}>", inline=True)
            embed.add_field(name="Moderator", value=f"<@{ctx.author.id}>", inline=True)
            embed.add_field(name="Reason", value="reason", inline=True)
            embed.set_footer(text=f"ID: {user.id}")
            await self.log_channel.send(embed=embed)

        else:
            await ctx.send(f"{user.display_name} could not be Banned.")

        await ctx.send("Action complete.")

    @ban_members.error
    async def ban_members_error(self,ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Insufficient permissions to perform that task.")

    @command(name="purge")
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, targets:Greedy[Member], limit: Optional[int] = 1):
        def _check(message):
            return not len(targets) or message.author in targets
        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit, check=_check)

                await ctx.send(f"Delted {len(deleted):,} messages.", delete_after=5)

        else:
            await ctx.send("The limit provided is not within acceptable bounds.")

    @command(name="mute")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def mute_members(self, ctx, targets: Greedy[Member], minutes: Optional[int], *, 
                           reason: Optional[str] = "no reason provided."):
        if not len(targets):
            await ctx.send("One or more required arguments missing.")

        else:
            unmutes = []

            for target in targets:
                if not self.mute_role in target.roles:
                    if ctx.guild.me.top_role.position > target.top_role.position:
                        role_ids = ",".join([str(r.id) for r in target.roles])
                        end_time = datetime.utcnow() + timedelta(seconds=minutes) if minutes else None

                        db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
                                    target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())

                        await target.edit(roles=[self.mute_role])

                        embed = Embed(title="Member muted",
                                              color=0xDD2222,
                                               timestamp = datetime.utcnow())

                        embed.set_thumbnail(url=target.avatar_url)

                        fields = [("Member", target.display_name, False),
                              ("Actioned by", ctx.author.display_name, False),
                              ("Duration", f"{minutes:,} hour(s)" if minutes else "Indefinite", False),
                              ("Reason", reason, False)]

                        for name, value, inline in fields:
                            embed.add_field(name=name, value=value, inline=inline)

                        await self.log_channel.send(embed=embed)

                        if minutes:
                            unmutes.append(target)

                    else:
                        await ctx.send(f"{target.display_name} could not be muted.")

                else:
                    await ctx.send(f"{target.display_name} is already muted.")
                        
            await ctx.send("action complete.")

            if len(unmutes):
                await sleep(minutes)
                await self.unmute(ctx, target)

    @mute_members.error
    async def mute_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Insufficent permissions to perform that task.")

    async def unmute(self, ctx, targets, *, reason="Mute time expired."):
        for target in targets:
            if self.mute_role in target.roles:
                role_ids = db.field("SELECT RoleIDs FROM mutes WHERE UserID = ?", target.id)
                roles = [ctx.guild.get_role(int(id )) for id in role_ids.split(",") if len(id )]

                db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)

                await target.edit(roles=roles)

                embed = Embed(title="Member Unmuted",
                                color=0xDD2222,
                                timestamp = datetime.utcnow())

                embed.set_thumbnail(url=target.avatar_url)

                fields = [("Member", target.display_name, False),
                          ("Reason", reason, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.log_channel.send(embed=embed)                

    @command(name="unmute")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def unmute_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "no reason provided."):
        if not len(targets):
            await ctx.send("One or more required arguments is missing.")

        else:
            await self.unmute(ctx, targets, reason=reason)

 

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.log_channel = self.bot.get_channel(808563375944106074)
            #pro life log channel: 808563375944106074
            #testing bot log channel: 828785261449445486
            self.mute_role = self.bot.guild.get_role(809094530631991297)
            #pro life mute role: 809094530631991297
            #testing bot mute role: 830127409008869397
            #self.bot.cogs_ready.ready_up("mod")


#    @Cog.listener()
#    async def on_message(self, message):
#        messageAuthor = message.author
 


def setup(bot):
    bot.add_cog(Mod(bot))