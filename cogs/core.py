#Modules
from typing import Any, Union
import discord
import requests
import json
from discord.embeds import Embed
from discord.ext import commands
from main import status, INFO, client, scheduler, USERS
from bank.bank import Customer

class Core(commands.Cog):

    def __init__(self, client) -> None:
        self.client = client

    @staticmethod
    def spy(ctx) -> Union[str, str]:
        """Saves info from new users and returns their mention code and locale.
        """
        id = ctx.author.id
        name = ctx.author.name
        mention = ctx.author.mention
        data = [str(id), str(name), str(mention)]
        data = ','.join(data)
        locale = ctx.guild.preferred_locale
        users = [lines.strip() for lines in open(USERS)] #Reads the file so that we don't have copys of users.
        for line in users: 
            #Searches in all of lines from the csv
            #then looks at the first info on the line that is the id
            #if the unique id has a match it means the user is already stored.
            if line.split(',')[0] == str(id):
                customer = Customer(id, name).add_credit(1)
                del customer
                return mention, locale, id
        else:
            open(USERS, 'a').write(f'{data}\n') #If the id is new we save it.
            customer = Customer(id, name).add_credit(1)
            del customer
            status('New user registered')
            return mention, locale, id

    @staticmethod
    async def embed(*, 
    title: str = None, description: str = Embed.Empty, 
    imageurl: str = None, footer: str = None, 
    fields: list = None, thumbnail: str = None,
    color: Any = Embed.Empty
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

    @staticmethod
    async def notifier(message: str, act: str) -> None:
        """Sends a message for all subscribed channels."""
        subs = [lines.strip() for lines in open(f'{INFO}/{act}.csv')]
        for line in subs[1:]:
            if line == '':
                continue
            else:
                line = line.split(',')
                channel = client.get_channel(int(line[0]))
                await channel.send(message)
                status('Notifying...')

    async def sound(self, ctx, path: str):
        """Plays a sound."""
        self.spy(ctx)
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