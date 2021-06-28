from os import stat
from discord.ext import commands
from .core import Core
from main import VERSION, spy, status, scheduler, FOOTER
from apscheduler.triggers.cron import CronTrigger
from discord.utils import get

def syntax(command):
    aliases = '|'.join([str(command), *command.aliases])
    params = []
    for key, value in command.params.items():
        params.append(f'[{key}]' if 'NoneType' in str(value) else f'<{key}>')
    params = ' '.join(params)
    return aliases, params

class General(Core):

    def __init__(self, client) -> None:
        super().__init__(client)
        self.client.remove_command('help')

    @commands.command()
    async def bot(self, ctx):
        """Informação rápida sobre o bot"""
        spy(ctx)
        thumbnail = self.client.user.avatar_url
        embed = await self.embed(
            title='NÉD Bot',
            description=f'Versão personalizada pro servidor da NÉD do bot (ainda não sei o nome kk)\n`Ver. {VERSION}`',
            footer='by Digão', thumbnail=thumbnail
            )
        await ctx.send(embed=embed)
        status()

    @commands.command()
    async def server(self, ctx):
        """Mostra informações sobre o servidor."""
        spy(ctx)
        name = str(ctx.guild.name)
        description = 'str(ctx.guild.description)'
        member_count = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        deus = await self.set_field('Deus dos Deuses', '<@688942919347863553>')
        mandato = await self.set_field('Mandato Atual', '<@268522466656124938>')
        representante = await self.set_field('Representante', '<@335679355646640139>')
        broxa = await self.set_field('Maior Broxa de Todos', '<@313175099047936003>')
        seguidores = await self.set_field('Seguidores do Culto', member_count)
        fields = [deus, mandato, representante, broxa, seguidores]
        embed = await self.embed(title=name, description=description, thumbnail=icon, fields=fields)
        await ctx.send(embed=embed)
        status('Informando sobre o server...')

    async def command_help(self, ctx, command):
        help = [await self.set_field(name='Command description', value=command.help)]
        aliases, params = syntax(command)
        embed = await self.embed(
            title=f'Help with ``{aliases}``', description=f'`{params}`',
            color=ctx.author.colour, footer=FOOTER, fields=help
            )
        await ctx.send(embed=embed)
        status('Helping...')

    async def general_help(self, ctx):
        fields = []
        for cmd in list(self.client.commands):
            if cmd.hidden:
                continue
            aliases = syntax(cmd)[0]
            fields.append(await self.set_field(name=f'``{aliases}``', value=f'{cmd.help}' or 'No description'))
        embed = await self.embed(
            title='Help',footer=FOOTER,
            color=ctx.author.colour, fields=fields)
        await ctx.send(embed=embed)
        status('Helping...')

    @commands.command(name='help', aliases=['ajuda'])
    async def show_help(self, ctx, command: str = None):
        """Shows this message."""
        spy(ctx)
        if command is None:
            await self.general_help(ctx)
        else:
            if (command := get(self.client.commands, name=command)):
                await self.command_help(ctx, command)
            else:
                await ctx.send('That command does not exist.')

    async def not_broxa(self, message='Lembrando que <@313175099047936003> é broxa', act='broxa'):
        status(message)
        await self.notifier(message, act)

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler.add_job(self.not_broxa, CronTrigger(hour=20,minute=30,second=0))
        scheduler.start()
        status('General schedulers started')

def setup(client):
    client.add_cog(General(client))