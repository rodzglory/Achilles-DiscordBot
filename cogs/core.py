import os
from typing import Any
import weakref
import discord
import requests
import json

from discord.embeds import Embed
from discord.ext import commands
from main import spy, status, INFO, client, scheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from time import sleep
from functools import wraps

class Core(commands.Cog):

    def __init__(self, client) -> None:
        self.client = client

    @staticmethod
    async def embed(*, 
    title: str = None, description: str = None, 
    imageurl: str = None, footer: str = None, 
    fields: list = None, thumbnail: str = None,
    color: Any = None
    ) -> Embed:
        """Helps at the creation of an Discord Embed object."""
        embed = discord.Embed(title=title, description=description, colour=color)
        if imageurl:
            embed.set_image(url=imageurl)
        if footer:
            embed.set_footer(text=footer)
        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        return embed

    @staticmethod
    async def set_field(*, name: str, value: Any, inline: bool = False) -> tuple:
        """Sets a tuple that contains the values needed for a field of the embed."""
        return (name, value, inline)

    async def notifier(self, message: str, act: str) -> None:
        """Sends a message for all subscribed channels."""
        subs = [lines.strip() for lines in open(f'{INFO}/{act}.csv')]
        for line in subs[1:]:
            if line == '':
                continue
            else:
                line = line.split(',')
                channel = self.client.get_channel(int(line[0]))
                await channel.send(message)
                status('Notifying...')

    async def sound(self, ctx, path: str):
        """Plays a sound."""
        spy(ctx)
        voice = ctx.voice_client
        if voice.is_playing():
            return await ctx.send('I\'m already playing something')
        audio = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path)) #Transforms the audio file into a object that Discord can play.
        voice.play(audio)
        status('Playing...')

    async def fecth_image(self, url: str, index: int = 0):
        """Fetches an image from a site."""
        image = []
        response = requests.get(url)
        data = json.loads(response.text)
        image.append(list(data.values())[index])
        return image