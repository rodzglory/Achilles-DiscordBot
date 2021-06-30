from os import stat
from discord.ext import commands
from .core import Core
from main import VERSION, spy, status, scheduler, FOOTER, BOT
from apscheduler.triggers.cron import CronTrigger
from discord.utils import get

def syntax(command):
    """`Does some magic!`
    By that it means it gets all the aliases and parameters from the command.
    """
    aliases = '|'.join([str(command), *command.aliases])
    params = []
    for key, value in command.params.items():
        #This where the magic happens and it stores all the info in the list.
        params.append(f'[{key}]' if 'NoneType' in str(value) else f'<{key}>')
    params = ' '.join(params)
    return aliases, params

class General(Core):

    def __init__(self, client) -> None:
        super().__init__(client)
        self.client.remove_command('help')

    @commands.command()
    async def bot(self, ctx):
        """Short info about the bot."""
        spy(ctx)
        thumbnail = self.client.user.avatar_url
        embed = await self.embed(
            title=BOT,
            description=f'Hi I am Achilles\n`Ver. {VERSION}`',
            footer=FOOTER, thumbnail=thumbnail
            )
        await ctx.send(embed=embed)
        status()

    async def command_help(self, ctx, command):
        """Gives more specific help on a specific command."""
        help = [await self.set_field(name='Command description', value=command.help)]
        aliases, params = syntax(command)
        embed = await self.embed(
            title=f'Help with ``{aliases}``', description=f'`{params}`',
            color=ctx.author.colour, footer=FOOTER, fields=help
            )
        await ctx.send(embed=embed)
        status('Helping...')

    async def general_help(self, ctx):
        """Gives help on all commands."""
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

    @commands.command(name='help')
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

    @commands.command(aliases = ['enter', 'join'])
    async def connect(self, ctx):
        """Joins the same channel of the user."""
        channel = ctx.message.author.voice.channel
        status(f'Joining the {channel}...')
        await channel.connect()

    @commands.command(aliases = ['leave', 'dc'])
    async def disconnect(self, ctx):
        """Disconnects the bots from the voice channel."""
        await ctx.voice_client.disconnect()

    @commands.Cog.listener()
    async def on_ready(self):
        status('General started')

def setup(client):
    client.add_cog(General(client))