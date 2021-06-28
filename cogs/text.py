import discord
import os

from typing import Optional
from discord.ext import commands
from discord.ext.commands.core import command
from .core import Core
from main import spy, status, TEXTS, VERSION, client, scheduler
from random import choice
from imdb import IMDb
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
#Kátia Flávia, a Godiva do Irajá
SHIS = os.path.join(TEXTS, 'shis.txt')
BROXAS = os.path.join(TEXTS, 'broxas.txt')
FRASES = os.path.join(TEXTS, 'frases.txt')
GUIZAO = '<@313175099047936003>'

ia = IMDb()

class Text(Core):

    def __init__(self, client) -> None:
        self.client = client

    @commands.command(aliases=['frase'])
    async def ned(self, ctx):
        """Fala uma frase da NÉD"""
        spy(ctx)
        frases = [line for line in open(FRASES, encoding='UTF-8')]
        await ctx.send(f'{choice(frases)}')
        status('Parafraseando...')

    @commands.command()
    async def shi(self, ctx):
        """Fala uma frase de algum filósofo"""
        spy(ctx)
        shis = [line for line in open(SHIS, encoding='UTF-8')]
        prefix = 'Já diria o Mestre Shi: '
        await ctx.send(f'{prefix} \n{choice(shis)}')
        status('Filosofando...')

    @commands.command()
    async def broxa(self, ctx):
        """Te lembra que o Guizão é broxa"""
        spy(ctx)
        broxas = [line for line in open(BROXAS, encoding='UTF-8')]
        await ctx.send(f'{GUIZAO} {choice(broxas)}')
        status('Broxando...')

    @commands.command(aliases=['film'])
    async def filme(self, ctx, qnt: Optional[int] = 1, *kw: str):
        """Te recomenda um filme (ou série) usando uma keyword de
        https://www.imdb.com/search/keyword/
        ou um filme (ou série) aleatório dos top 250 (só deixar em branco depois de filme)
        """
        mention = spy(ctx)[0]
        films = []
        if not kw:
            movies = ia.get_top250_movies()
            status(f'Escolhendo um filme de {len(movies)}...')
            for x in range(qnt):
                await ctx.send(f'{mention}, escolhi este filme (ou talvez série): `{choice(movies)}`')
        else:
            kw_joined = '-'.join(kw)
            kw = ' '.join(kw)
            movies = []
            await ctx.send('Pesquisando, aguarde...')
            for page in range(10):
                for movie in ia.get_keyword(kw_joined, page=page):
                    movies.append(movie)
            print(len(movies))
            await ctx.channel.purge(limit=1)
            if movies == []:
                return await ctx.send(f'Não encontrei nada com {kw}')
            status(f'Escolhendo um filme de {len(movies)}...')
            for x in range(qnt):
                await ctx.send(f'{mention}, escolhi este filme (ou talvez série): `{choice(movies)}`')

def setup(client):
    client.add_cog(Text(client))