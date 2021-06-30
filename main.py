#Modules
import os
from typing import Union
import discord
from discord import activity
from discord import channel
from discord import message
from discord.ext import commands
from time import sleep, localtime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from random import choice

#Constants
BOT = 'Achilles'
VERSION = '0.1.1'
#Paths
BOTDIR = os.path.dirname(__file__)
INFO = os.path.join(BOTDIR, 'infos') 
TOKEN = open(f'{INFO}/botinfo.txt').readlines()[0]
PREFIXES = open(f'{INFO}/botinfo.txt').readlines()[1].strip().split(',') 
COGS = os.path.join(BOTDIR, 'cogs')
IMAGES = os.path.join(BOTDIR, 'images')
SUBBED = os.path.join(INFO, 'subbed.csv')
USERS = os.path.join(INFO, 'users.csv')
TEXTS = os.path.join(BOTDIR, 'texts')
ACTIVITIES = os.path.join(INFO, 'activities.txt')
AUDIO = os.path.join(BOTDIR, 'audio')
SAMPLE = os.path.join(AUDIO, 'sample')
#Objects
client = commands.Bot(command_prefix=PREFIXES) #Calls the bot object, the most important thing to make the bot work.
scheduler = AsyncIOScheduler() #Scheduler for automated tasks.

def status(message: str = 'Probably forgot the status...') -> print:
    """Changes the console status.
    """
    print(f'{message} {localtime()[3]}:{localtime()[4]}:{localtime()[5]}') #hours:mins:secs
    print('\nAwaiting command...')

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
            return mention, locale
    else:
        open(USERS, 'a').write(f'{data}\n') #If the id is new we save it.
        status('New user registered')
        return mention, locale

async def activity_changer() -> None: #This is the "status" under the bot name.
    """Changes the bot activity.
    """ 
    name = choice(open(ACTIVITIES, 'r', encoding='UTF-8').readlines()) #Randomly chooses one of the activities in the activities file.
    activity = discord.Activity(name=name, type=discord.ActivityType.watching) #Transforms it into the discord class.
    await client.change_presence(activity=activity)

@client.event #Decorator that gives a flag on event.
async def on_ready() -> None: #When the bot is ready for using.
    """Notifies when it's ready and turn on schedulers."""
    status(f'\n{client.user.name} is on')
    await activity_changer()
    scheduler.add_job(activity_changer, CronTrigger(minute=30, second=0)) #Creates a scheduled task, this one changes activity every 30 mins.
    scheduler.start()
    status('Schedulers started')

@client.command(hidden=True) #This is a Discord command, won't show on the help command.
@commands.has_permissions(administrator=True) #Checks if the user that called it has the permission administrator.
async def reload(ctx, extension) -> None:
    """Reloads a cog."""
    spy(ctx)
    client.reload_extension(f'cogs.{extension}')
    status(f'Reloading {extension}...')
    await ctx.send(f'{extension} reloaded') #Bot sends a message to the same text channel it was called.

@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def load(ctx, extension) -> None:
    """Loads an unloaded cog."""
    spy(ctx)
    client.load_extension(f'cogs.{extension}')
    status(f'Loading {extension}...')
    await ctx.send(f'{extension} loaded')

@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def unload(ctx, extension) -> None:
    """Unloads a loaded cog."""
    spy(ctx)
    client.unload_extension(f'cogs.{extension}')
    status(f'Unloading {extension}...')
    await ctx.send(f'{extension} unloaded')

@client.command(aliases=['clear'])
@commands.has_permissions(manage_messages=True) #Bot needs this server permission, I don't recommend removing this check.
async def purge(ctx, amt=100) -> None:
    """Clears channel of an amount (default 100) of messages,
    needs `manage messages` permission.
    """
    spy(ctx)
    await ctx.channel.purge(limit = amt + 1) #limit is the amount of messages the bot will clear + 1 for the command.
    await ctx.send(f'The last {amt} messages were purged')
    status(f'Purging {amt}...')

@client.command()
@commands.has_permissions(administrator=True)
async def subscribe(ctx, act: str) -> None:
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

@client.command()
@commands.has_permissions(administrator=True)
async def unsubscribe(ctx, act: str) -> None:
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

if __name__ == '__main__': #Makes it can't be run through imports.

    os.system('cls||clear') #Clear the console for easier visualization.

    print('='*50)
    print(f'Welcome to {BOT} bot Ver. {VERSION}')
    print('='*50)
    sleep(0.5)

    os.system('cls||clear')

    for file in os.listdir(COGS):
        #It looks for every file in the cogs folder
        #then checks if it ends with py, if it does loads it
        #if the file starts with # or is the core module it's no implemented.
        if file.endswith('.py'):
            if file.startswith('core') or file.startswith('#'): # # was arbritary it can be anything else or even nothing.
                continue
            else:
                client.load_extension(f'cogs.{file[:-3]}')
                print(f'Loading {file[:-3]} extension...')
                sleep(0.25)

    os.system('cls||clear')

    client.run(TOKEN) #Runs the bot.