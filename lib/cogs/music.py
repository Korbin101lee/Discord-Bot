import asyncio
import datetime as dt
import enum
import random
import re
import typing as t
from enum import Enum
import os
from os.path import isfile
from sqlite3 import connect
from apscheduler.triggers.cron import CronTrigger

from os import system

from lib.db import db
DB_PATH = "./data/db/songs.db"
BUILD_PATH = "./data/db/build_songs.sql"

cxn2 = connect(DB_PATH, check_same_thread=False)
cur2 = cxn2.cursor()


def with_commit2(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner


@with_commit2
def build2():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)


def commit():
    cxn2.commit()


def autosave(sched):
    sched.add_job(commit, CronTrigger(second=0))



def close():
    cxn2.close()


def field(command, *values):
    cur2.execute(command,tuple(values))

    if (fetch := cur2.fetchone()) is not None:
        return fetch[0]


def record(command, *values):
    cur2.execute(command,tuple(values))


    return cur2.fetchone()


def records(command, *values):
    cur2.execute(command,tuple(values))

    return cur2.fetchall()

def column(command, *values):
    cur2.execute(command,tuple(values))

    return [item[0] for item in cur2.fetchall()]


def execute(command, *values):
	cur2.execute(command, tuple(values))


def multiexec(command,valueset):
    cur2.executemany(command,valueset)


def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur2.executescript(script.read())

import aiohttp
import discord
import wavelink
from discord.ext import commands
URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
LYRICS_URL = "https://some-random-api.ml/lyrics?title="
HZ_BANDS = (20, 40, 63, 100, 150, 250, 400, 450, 630, 1000, 1600, 2500, 4000, 10000, 16000)
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}




class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class VolumeTooLow(commands.CommandError):
    pass


class VolumeTooHigh(commands.CommandError):
    pass


class MaxVolume(commands.CommandError):
    pass


class MinVolume(commands.CommandError):
    pass


class NoLyricsFound(commands.CommandError):
    pass


class InvalidEQPreset(commands.CommandError):
    pass


class NonExistentEQBand(commands.CommandError):
    pass


class EQGainOutOfBounds(commands.CommandError):
    pass


class InvalidTimeString(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.eq_levels = [0.] * 15

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            cur2.execute("DELETE FROM music_player")
            cxn2.commit()
            await self.destroy()

        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound
    

        
        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        else:            
            self.queue.add(tracks[0])

            embed=discord.Embed(title=f"{tracks[0].title}", url=f"{tracks[0].uri}")
            embed.set_author(name="Added to queue", icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url=f"{tracks[0].thumb}")
            #Track_Url
            cur2.execute("UPDATE music_player SET Track_Thumbnail = ?, Track_Url = ? WHERE Num = (SELECT MAX(Num) FROM music_player)", ([tracks[0].thumb, tracks[0].uri]))                
            cxn2.commit()
            embed.add_field(name="Author", value=f"{tracks[0].author}", inline=True)
            conver_seconds = tracks[0].length / 1000
            m1, s1 = divmod(int(conver_seconds), 60)
            song_length = f'{m1}:{s1:02}'
            embed.add_field(name="Song Duration", value=song_length, inline=True)
            PosInQueue = self.queue.length
            embed.add_field(name="Position in queue", value=str(PosInQueue), inline=True)

                
            await ctx.send(embed=embed)
                #await ctx.send(f"Added {tracks[0].uri} to the queue") #{tracks[0].uri} to the queue.
        
        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )#returns the emoji you selected with the song

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:

                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node `{node.identifier}` ready.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs.")
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "europe",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name="connect", aliases=["join"])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        server_name = str(ctx.guild)
        server_id = ctx.guild.id
        Num = 0
        #cur2.execute(f'delete from music_player where Server_ID ="{server_id}" and Server_Name = "{server_name}"')
        #cxn2.commit()
        user_name = str(ctx.message.author)
        queue_name = f"Queue#{server_id}"
        song_name = f"Song#{server_id}"
        channel_id = ctx.message.author.voice.channel.id
        channel_name = str(ctx.message.author.voice.channel)
        qeue_num = 1
        #thistuple = ("Num", "Server_ID", "Server_Name", "Voice_ID", "Voice_Name", "User_Name", "Next_Queue", "Queue_Name", "Song_Name")

        #cur2.execute("insert into music_player(Num, Server_ID, Server_Name, Voice_ID, Voice_Name, User_Name, Next_Queue, Queue_Name, Song_Name) values(?, ?,?,?,?,?,?,?,?)",
        #(Num, server_id, server_name, channel_id, channel_name, user_name, qeue_num , queue_name, song_name))
        #cxn2.commit()

        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.send(f"Connected to {channel.name}.")

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send("Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")

    @commands.command(name="disconnect", aliases=["leave"])
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send("Disconnected.")

    @commands.command(name="play", aliases=["p"])
    async def play_command(self, ctx, *, query: t.Optional[str]):

        server_name = str(ctx.guild)
        server_id = ctx.guild.id
        channel_id = ctx.message.author.voice.channel.id
        channel_name = str(ctx.message.author.voice.channel)



        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send("Playback resumed.")

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                await ctx.send(f":musical_note: Searching :mag_right: `{query}`")
                print (query)
                cur2.execute("INSERT INTO music_player (User_Name, Song_Name) VALUES(?, ?)", (str(ctx.message.author), query))
                #cur2.execute(f"INSERT INTO music_player(Song_Name) VALUES('{query}')")
                cxn2.commit()

                query = f"ytsearch:{query}"
            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))
#	db.execute(f"INSERT OR IGNORE INTO guilds(GuildID) VALUES({message.guild.id})")

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("No songs to play as the queue is empty.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")

    @commands.command(name="pause")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.send("Playback paused.")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("Already paused.")

    @commands.command(name="stop", aliases=["clear"])
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.send("Playback stopped.")

    @commands.command(name="next", aliases=["skip", "s"])
    async def next_command(self, ctx):
        player = self.get_player(ctx)

        cur2.execute("DELETE FROM music_player WHERE Num in (select Num FROM music_player LIMIT 1)")
        cxn2.commit()


        await player.stop()
        await ctx.send("Playing next track in queue.")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("There are no more tracks in the queue.")

    @commands.command(name="previous")
    async def previous_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        await ctx.send("Playing previous track in queue.")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send("There are no previous tracks in the queue.")

    @commands.command(name="shuffle")
    async def shuffle_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.send("Queue shuffled.")

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue could not be shuffled as it is currently empty.")

    @commands.command(name="repeat")
    async def repeat_command(self, ctx, mode: str):
        if mode not in ("none", "1", "all"):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        await ctx.send(f"The repeat mode has been set to {mode}.")

    @commands.command(name="queue", aliases=["q"])
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        song_url = field("SELECT Track_Url FROM music_player")

        embed = discord.Embed(
            title=f"Queue for {ctx.guild.name}", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            colour=0xAD23D7,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="__Now Playing:__",
            value=f'[{getattr(player.queue.current_track, "title", "No tracks currently playing.")}]({song_url}) | ',
            inline=False
        )
        print(player.queue.current_track)

        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="__Up Next:__",            
                    value=f"\n".join(t.title for t in upcoming[:show]),
                inline=False
            )

        msg = await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is currently empty.")

    # Requests -----------------------------------------------------------------

    @commands.group(name="volume", invoke_without_command=True)
    async def volume_group(self, ctx, volume: int):
        player = self.get_player(ctx)

        if volume < 0:
            raise VolumeTooLow

        if volume > 150:
            raise VolumeTooHigh

        await player.set_volume(volume)
        await ctx.send(f"Volume set to {volume:,}%")

    @volume_group.error
    async def volume_group_error(self, ctx, exc):
        if isinstance(exc, VolumeTooLow):
            await ctx.send("The volume must be 0% or above.")
        elif isinstance(exc, VolumeTooHigh):
            await ctx.send("The volume must be 150% or below.")

    @volume_group.command(name="up")
    async def volume_up_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 150:
            raise MaxVolume

        await player.set_volume(value := min(player.volume + 10, 150))
        await ctx.send(f"Volume set to {value:,}%")

    @volume_up_command.error
    async def volume_up_command_error(self, ctx, exc):
        if isinstance(exc, MaxVolume):
            await ctx.send("The player is already at max volume.")

    @volume_group.command(name="down")
    async def volume_down_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 0:
            raise MinVolume

        await player.set_volume(value := max(0, player.volume - 10))
        await ctx.send(f"Volume set to {value:,}%")

    @volume_down_command.error
    async def volume_down_command_error(self, ctx, exc):
        if isinstance(exc, MinVolume):
            await ctx.send("The player is already at min volume.")

    @commands.command(name="lyrics")
    async def lyrics_command(self, ctx, name: t.Optional[str]):
        player = self.get_player(ctx)
        name = name or player.queue.current_track.title

        async with ctx.typing():
            async with aiohttp.request("GET", LYRICS_URL + name, headers={}) as r:
                if not 200 <= r.status <= 299:
                    raise NoLyricsFound

                data = await r.json()

                if len(data["lyrics"]) > 2000:
                    return await ctx.send(f"<{data['links']['genius']}>")

                embed = discord.Embed(
                    title=data["title"],
                    description=data["lyrics"],
                    colour=ctx.author.colour,
                    timestamp=dt.datetime.utcnow(),
                )
                embed.set_thumbnail(url=data["thumbnail"]["genius"])
                embed.set_author(name=data["author"])
                await ctx.send(embed=embed)

    @lyrics_command.error
    async def lyrics_command_error(self, ctx, exc):
        if isinstance(exc, NoLyricsFound):
            await ctx.send("No lyrics could be found.")

    @commands.command(name="eq")
    async def eq_command(self, ctx, preset: str):
        player = self.get_player(ctx)

        eq = getattr(wavelink.eqs.Equalizer, preset, None)
        if not eq:
            raise InvalidEQPreset

        await player.set_eq(eq())
        await ctx.send(f"Equaliser adjusted to the {preset} preset.")

    @eq_command.error
    async def eq_command_error(self, ctx, exc):
        if isinstance(exc, InvalidEQPreset):
            await ctx.send("The EQ preset must be either 'flat', 'boost', 'metal', or 'piano'.")

    @commands.command(name="adveq", aliases=["aeq"])
    async def adveq_command(self, ctx, band: int, gain: float):
        player = self.get_player(ctx)

        if not 1 <= band <= 15 and band not in HZ_BANDS:
            raise NonExistentEQBand

        if band > 15:
            band = HZ_BANDS.index(band) + 1

        if abs(gain) > 10:
            raise EQGainOutOfBounds

        player.eq_levels[band - 1] = gain / 10
        eq = wavelink.eqs.Equalizer(levels=[(i, gain) for i, gain in enumerate(player.eq_levels)])
        await player.set_eq(eq)
        await ctx.send("Equaliser adjusted.")

    @adveq_command.error
    async def adveq_command_error(self, ctx, exc):
        if isinstance(exc, NonExistentEQBand):
            await ctx.send(
                "This is a 15 band equaliser -- the band number should be between 1 and 15, or one of the following "
                "frequencies: " + ", ".join(str(b) for b in HZ_BANDS)
            )
        elif isinstance(exc, EQGainOutOfBounds):
            await ctx.send("The EQ gain for any band should be between 10 dB and -10 dB.")

    @commands.command(name="playing", aliases=["np"])
    async def playing_command(self, ctx):
        player = self.get_player(ctx)

        if not player.is_playing:
            raise PlayerIsAlreadyPaused
        name = field("SELECT User_Name FROM music_player")

        position = divmod(player.position, 60000)
        length = divmod(player.queue.current_track.length, 60000)

        embed = discord.Embed(
            title=f"{player.queue.current_track.title}",
            url=f"{player.queue.current_track.uri}",
            description = f"`{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}`\n\n`Requested by:` {name}",
            colour=0x3498db,
        )
        embed.set_author(name="Now Playing ♪", icon_url="https://cdn.discordapp.com/avatars/828751134071717888/4d74c445b46ea32c77f88f241ba574c3.webp?size=1024")


        thumnail = field("SELECT Track_Thumbnail FROM music_player")

        embed.set_thumbnail(url=f"{thumnail}")

        #embed.add_field(name=f"`Requested by:`", value=f"{name}", inline=True)
        #  \u200b 

        await ctx.send(embed=embed)

    @playing_command.error
    async def playing_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("There is no track currently playing.")

    @commands.command(name="skipto", aliases=["playindex"])
    async def skipto_command(self, ctx, index: int):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not 0 <= index <= player.queue.length:
            raise NoMoreTracks

        player.queue.position = index - 2
        await player.stop()
        await ctx.send(f"Playing track in position {index}.")

    @skipto_command.error
    async def skipto_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("There are no tracks in the queue.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("That index is out of the bounds of the queue.")

    @commands.command(name="restart")
    async def restart_command(self, ctx):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        await player.seek(0)
        await ctx.send("Track restarted.")

    @restart_command.error
    async def restart_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("There are no tracks in the queue.")

    @commands.command(name="seek")
    async def seek_command(self, ctx, position: str):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not (match := re.match(TIME_REGEX, position)):
            raise InvalidTimeString

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        await ctx.send("Seeked.")


def setup(bot):
    bot.add_cog(Music(bot))