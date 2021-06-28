import os
from typing import Any
import weakref
import discord

from discord.embeds import Embed
from discord.ext import commands
from main import status, INFO, client, scheduler
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
    async def set_field(*, name: str, value: Any, inline: bool = False):
        return (name, value, inline)

    async def notifier(self, message: str, act: str) -> None:
        subs = [lines.strip() for lines in open(f'{INFO}/{act}.csv')]
        for line in subs[1:]:
            if line == '':
                continue
            else:
                line = line.split(',')
                channel = self.client.get_channel(int(line[0]))
                await channel.send(message)
                status('Notifying...')
