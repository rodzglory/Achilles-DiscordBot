from os import stat
from discord.ext import commands
from .core import Core
from main import VERSION, spy, status, scheduler, BOT, INFO
from apscheduler.triggers.cron import CronTrigger
from discord.utils import get

FOOTER = 'Powered by Achilles Bot'

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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def subscribe(self, ctx, act: str) -> None:
        """Subscribes the channel to notifications, needs admin permission."""
        spy(ctx)
        id = str(ctx.channel.id)
        name = str(ctx.channel.name)
        guild = str(ctx.channel.guild)
        data = [id, name, guild]
        data = ','.join(data)
        try:
            file = open(f'{INFO}/{act}.csv')
            subs = [lines.strip() for lines in file]
            for line in subs:
                #Searches in all of lines from the csv
                #then looks at the first info on the line that is the id
                #if the unique id has a match it means the channel is already stored.
                if line.split(',')[0] == id:
                    await ctx.send('Channel already subscribed')
                    return status('Oops')
            else: #If the id is new we save it.
                open(f'{INFO}/{act}.csv', 'a', encoding='UTF-8').write(f'{data}\n')
                status(f'Subscribing {name} to {act}, from {guild}')
                await ctx.send(f'Channel {name} subscribed to {act} successfully')
        except FileNotFoundError: #If the act doesn't exist creates a new csv named by it with the channel.
            file = open(f'{INFO}/{act}.csv', 'w', encoding='UTF-8').write(f'id,name,guild\n{data}\n')
            status(f'Subscribing {name} to {act}, from {guild}')
            await ctx.send(f'Channel {name} subscribed to {act} successfully')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unsubscribe(self, ctx, act: str) -> None:
        """Unsubs the channel from notifications, needs admin permission."""
        spy(ctx)
        id = str(ctx.channel.id)
        try:
            file = open(f'{INFO}/{act}.csv', 'r')
            subs = [lines.strip() for lines in file]
            for line in subs:
                if line.split(',')[0] == id:
                    del(line)
            file = open(f'{INFO}/{act}.csv', 'w')
            for line in subs:
                file.write(f'{line}\n')
                await ctx.send('Channel unsubbed')
        except FileNotFoundError:
            await ctx.send(f'{act} does not exist')

    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True) #Bot needs this server permission, I don't recommend removing this check.
    async def purge(self, ctx, amt=100) -> None:
        """Clears channel of an amount (default 100) of messages,
        needs `manage messages` permission.
        """
        spy(ctx)
        await ctx.channel.purge(limit = amt + 1) #limit is the amount of messages the bot will clear + 1 for the command.
        await ctx.send(f'The last {amt} messages were purged')
        status(f'Purging {amt}...')

    @commands.command(hidden=True) #This is a Discord command, won't show on the help command.
    @commands.has_permissions(administrator=True) #Checks if the user that called it has the permission administrator.
    async def reload(self, ctx, extension) -> None:
        """Reloads a cog."""
        spy(ctx)
        self.client.reload_extension(f'cogs.{extension}')
        status(f'Reloading {extension}...')
        await ctx.send(f'{extension} reloaded') #Bot sends a message to the same text channel it was called.

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, extension) -> None:
        """Loads an unloaded cog."""
        spy(ctx)
        self.client.load_extension(f'cogs.{extension}')
        status(f'Loading {extension}...')
        await ctx.send(f'{extension} loaded')

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension) -> None:
        """Unloads a loaded cog."""
        spy(ctx)
        self.client.unload_extension(f'cogs.{extension}')
        status(f'Unloading {extension}...')
        await ctx.send(f'{extension} unloaded')

    @commands.Cog.listener()
    async def on_ready(self):
        status('General started')

def setup(client):
    client.add_cog(General(client))