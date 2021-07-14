from discord.ext import commands
import discord
from discord.utils import get
from .core import Core
from main import status

FOOTER = 'Powered by Achilles Bot'

class Help(Core):

    def __init__(self, client) -> None:
        super().__init__(client)
        self.client.remove_command('help')

    @staticmethod
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

    async def command_help(self, ctx, command):
        """Gives more specific help on a specific command."""
        help = [await self.set_field(name='Command description', value=command.help)]
        aliases, params = self.syntax(command)
        embed = await self.embed(
            title=f'Help with ``{aliases}``', description=f'`{params}`',
            color=ctx.author.colour, footer=FOOTER, fields=help
            )
        await ctx.send(embed=embed)
        status('Helping...')

    async def general_help(self, ctx):
        """Gives help on all commands."""
        fields = []
        cogs_names = []
        sorted_commands_by_cogs = {}
        embed_max = 61
        limit = embed_max - embed_max//5
        for cmd in self.client.commands:
            cog_name = cmd.module[5:].capitalize()
            if cmd.hidden:
                continue
            elif cog_name in cogs_names:
                continue
            else:
                cogs_names.append(cog_name)
        cogs_names.sort()
        for name in cogs_names:
            cogs_commands = []
            for cmd in self.client.commands:
                if name == cmd.module[5:].capitalize():
                    cmd_name = str(cmd)
                    if len(cmd_name) < (embed_max//5):
                        trail = (embed_max//5) - len(cmd_name)
                        cmd_name = cmd_name + f' '*trail
                    cmd_help = cmd.help
                    if cmd_help is None:
                        cmd_help = 'No description'
                    cmd_info = cmd_name + f' - {cmd_help}'
                    if len(cmd_info) > embed_max:
                        cmd_info = cmd_info[:limit] + ' ... '
                    cogs_commands.append(cmd_info)
                else: continue
                cogs_commands.sort()
                sorted_commands_by_cogs[name] = cogs_commands
        for module in sorted_commands_by_cogs.items():
            module_name = module[0]
            cmds = '\n'.join(module[1])
            fields.append(await self.set_field(name=f'{module_name}', value=f'```{cmds}```'))
        embed = await self.embed(
            title='Help',footer='For more help use the command help followed by the command name',
            color=ctx.author.colour, fields=fields,
            description='```command      - description```')
        await ctx.send(embed=embed)
        status('Helping...')

    @commands.command(name='help')
    async def show_help(self, ctx, command: str = None):
        """Shows this message."""
        self.spy(ctx)
        if command is None:
            await self.general_help(ctx)
        else:
            if (command := get(self.client.commands, name=command)):
                await self.command_help(ctx, command)
            else:
                await ctx.send('That command does not exist.')

def setup(client):
    client.add_cog(Help(client))