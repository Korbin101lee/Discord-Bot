from typing import Optional

from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext.commands import command
import discord
from discord.ext.commands import command, has_permissions, bot_has_permissions

def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")
    params = " ".join(params)

    return f"```{cmd_and_aliases} {params}```"



class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=3)

    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(title = "Help",
                      description="Welcome to the Pro-Life help dialog!",
                      color=self.ctx.author.color)
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(text=f"{offset:,} = {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed


    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append((entry.brief or "No description", syntax(entry)))

        return await self.write_page(menu, fields)





class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help with '{command}'",
                      description=syntax(command),
                      color=ctx.author.color)
        embed.add_field(name="Command description", value=command.help)
        await ctx.send(embed=embed)

    """@command(name="help")
    async def show_help(self, ctx, cmd: Optional[str]):
        if cmd is None:
            menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)),            
                            delete_message_after=True,
                             timeout=60.0)
            await menu.start(ctx)


        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)

            else:
                await ctx.send("That command does not exist.")"""
    #@Cog.listener()
    #async def on_ready(self):
        #if not self.bot.ready:
            #self.bot.cogs_ready.ready_up("help")

    @command(name="help_fun")
    async def help_fun(self, ctx):
        embed=discord.Embed(color=ctx.message.author.color)
        embed.set_author(name="Fun Plugin")
        embed.add_field(name="+Roll [number]d[number]", value="rolls a dice to add them together", inline=False)
        embed.add_field(name="+Slap_member [user] [reason]", value="Slaps a member in the server", inline=False)
        embed.add_field(name="+Fact [animal]", value="get an animal fact from dog, cat, panda, fox, bird, koala", inline=False)
        await ctx.send(embed=embed)

    @command(name="help_info")
    async def help_info(self, ctx):
            embed=discord.Embed(color=ctx.message.author.color)
            embed.set_author(name="+Info Plugin")
            embed.add_field(name="+UserInfo [member]", value="get's info the the given member", inline=False)
            embed.add_field(name="+ServerInfo", value="Get's info of the given server", inline=False)
            await ctx.send(embed=embed)  

    @command(name="help_mod")
    @has_permissions(manage_messages=True)
    async def help_mod(self, ctx):
        embed=discord.Embed(color=ctx.message.author.color)
        embed.set_author(name="Mod Plugin")
        embed.add_field(name="+Kick [member] [reason]", value="Kicks a given member from the server", inline=False)
        embed.add_field(name="+Ban [member] [reason]", value="Bans a given member from the server", inline=False)
        embed.add_field(name="+Purge [limit]", value="Deletes a given amount of messages from the server", inline=False)
        embed.add_field(name="+Mute [user] [minutes] [reason]", value="Mutes a given member for a certain amount of time", inline=False)
        embed.add_field(name="+Unmute [user] [reason]", value="Unmutes a given member from the server", inline=False)
        embed.add_field(name="+Addprofanity [words]", value="Adds profanity to the server to delete certain messages", inline=False)
        embed.add_field(name="+Delprofanity [words]", value="Deletes progranity from the server to allow for certain words", inline=False)
        await ctx.send(embed=embed)

    @command(name="help_music")
    async def help_music(self, ctx):
        embed=discord.Embed(color=ctx.message.author.color)
        embed.set_author(name="Music Plugin")
        embed.add_field(name="+Join", value="Connects the bot to the channel you are in", inline=False)
        embed.add_field(name="+Leave", value="Disconnects the bot from the channel you are in", inline=False)
        embed.add_field(name="+Play [song]", value="Plays a song or adds it to the queue", inline=False)
        embed.add_field(name="+Pause", value="Pauses the song", inline=False)
        embed.add_field(name="+Resume", value="Resumes the song", inline=False)
        embed.add_field(name="+Clear", value="Clears all the songs from the queue", inline=False)
        embed.add_field(name="+Clear", value="Clears all Songs from playback", inline=False)
        embed.add_field(name="+Skip", value="Skips the song", inline=False)
        embed.add_field(name="+Previous", value="Plays the previous song", inline=False)
        embed.add_field(name="+Shuffle", value="shuffles the queue", inline=False)
        embed.add_field(name="+Repeat", value="repeats the queue", inline=False)
        embed.add_field(name="+Queue", value="shows the bot's music queue", inline=False)
        embed.add_field(name="+np", value="shows the song that is now playing", inline=False)
        embed.add_field(name="+Volume", value="Changes Bot volume for the group from 0-150", inline=False)
        embed.add_field(name="+Lyrics", value="Displays Lyrics of a song", inline=False)
        embed.add_field(name="+Eq", value="Sets eq modes on the mode(flat, boost, metal, piano)", inline=False)
        embed.add_field(name="+adveq", value="Advanced eq allows you to change the vand and gain", inline=False)
        embed.add_field(name="+skipto", value="Allows you to skip to a certain song in the que", inline=False)
        embed.add_field(name="+restart", value="restarts the song currently playing", inline=False)
        embed.add_field(name="+seek", value="seeks a time position in the current song playing", inline=False)

        await ctx.send(embed=embed)

    @command(name="help")
    async def help_commands(self, ctx):
        embed=discord.Embed(color=ctx.message.author.color)
        embed.set_author(name="Pro-Life Plugins Commands", icon_url="https://cdn.discordapp.com/avatars/828751134071717888/4d74c445b46ea32c77f88f241ba574c3.webp?size=1024")
        embed.add_field(name="Fun", value="`help_fun`", inline=True)
        embed.add_field(name="info", value="`help_info`", inline=True)
        if ctx.message.author.guild_permissions.manage_messages:
            embed.add_field(name="Mod", value="`help_mod`", inline=True)
        embed.add_field(name="Music", value="`help_music`", inline=True)
        await ctx.send(embed=embed)
        

        


def setup(bot):
    bot.add_cog(Help(bot))