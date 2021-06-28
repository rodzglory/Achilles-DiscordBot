#Modules
import os
import discord
from discord import activity
from discord import channel
from discord import message
from discord.ext import commands
from time import sleep, localtime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from random import choice

BOT = 'Achilles' #Bot's name
BOTDIR = os.path.dirname(__file__) #Bot's directory
INFO = os.path.join(BOTDIR, 'infos') #save the infos folder
TOKEN = open(f'{INFO}/botinfo.txt').readlines()[0] #gets the bot token in the botinfo file
PREFIXES = open(f'{INFO}/botinfo.txt').readlines()[1].strip().split(',') #gets the prefixes
COGS = os.path.join(BOTDIR, 'cogs') #cogs folder
IMAGES = os.path.join(BOTDIR, 'images') #images folder
ICON = os.path.join(BOTDIR, 'images/achilles.jpg') #bot default icon
SUBBED = os.path.join(INFO, 'subbed.csv') #template for saved subbed channels
USERS = os.path.join(INFO, 'users.csv') #template for infos saved from users
TEXTS = os.path.join(BOTDIR, 'texts') #folder with plain texts
ACTIVITIES = os.path.join(INFO, 'activities.txt') #template for activities
VERSION = '0.0.8a' #bot version
FOOTER = 'Achilles Bot' #footer for embed

client = commands.Bot(command_prefix=PREFIXES) #calls the bot object, the most important thing to make the bot work
scheduler = AsyncIOScheduler() #scheduler for automated tasks

def status(message: str = 'Probably forgot the status...') -> print:
    """Changes the console status
    """
    print(f'{message} {localtime()[3]}:{localtime()[4]}:{localtime()[5]}')
    print('\nAwaiting command...')

def spy(ctx) -> str:
    """Save new users of the bot
    """
    id = ctx.author.id
    name = ctx.author.name
    mention = ctx.author.mention
    data = [str(id), str(name), str(mention)]
    data = ','.join(data)
    locale = ctx.guild.preferred_locale
    users = [lines.strip() for lines in open(USERS)]
    for line in users:
        for row in line.split(','):
            if str(id) == row:
                return mention, locale
    else:
        open(USERS, 'a').write(f'{data}\n')
        status('New user registered')
        return mention, locale

@client.event
async def on_ready() -> None:
    """Notifies when it's ready and turn on schedulers"""
    status(f'\n{client.user.name} is on')
    await activity_changer()
    #schedulers on ready
    scheduler.add_job(activity_changer, CronTrigger(minute=30, second=0))
    scheduler.start()
    status('Schedulers started')
# TODO: Better list of random activities
@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def reload(ctx, extension) -> None:
    """Reloads a cog"""
    client.reload_extension(f'cogs.{extension}')
    status(f'Reloading {extension}...')
    await ctx.send(f'{extension} reloaded')

@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def load(ctx, extension) -> None:
    """Loads an unloaded cog"""
    client.load_extension(f'cogs.{extension}')
    status(f'Loading {extension}...')
    await ctx.send(f'{extension} loaded')

@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def unload(ctx, extension) -> None:
    """Unloads a loaded cog"""
    client.unload_extension(f'cogs.{extension}')
    status(f'Unloading {extension}...')
    await ctx.send(f'{extension} unloaded')

@client.command(aliases=['clear'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amt=100) -> None:
    """Clears channel of an amount (default 100) of messages, needs manage messages permission"""
    spy(ctx)
    await ctx.channel.purge(limit = amt + 1)
    await ctx.send(f'The last {amt} messages were purged')
    status(f'Purging {amt}...')

@client.command()
@commands.has_permissions(administrator=True)
async def subscribe(ctx, act: str) -> None:
    """Subscribes the channel to notifications, needs admin permission"""
    spy(ctx)
    channel = str(ctx.channel.id)
    name = str(ctx.channel.name)
    guild = str(ctx.channel.guild)
    data = [channel, name, guild]
    data = ','.join(data)
    try:
        file = open(f'{INFO}/{act}.csv')
        subs = [lines.strip() for lines in file]
        for line in subs:
            for row in line.split(','):
                if channel == row:
                    await ctx.send('Channel already subscribed')
                    return status('Oops')
        else:
            open(f'{INFO}/{act}.csv', 'a', encoding='UTF-8').write(f'{data}\n')
            status(f'Subscribing {name} to {act}, from {guild}')
            await ctx.send(f'Channel {name} subscribed to {act} successfully')
    except FileNotFoundError:
        file = open(f'{INFO}/{act}.csv', 'w', encoding='UTF-8').write(f'id,name,guild\n{data}\n')
        status(f'Subscribing {name} to {act}, from {guild}')
        await ctx.send(f'Channel {name} subscribed to {act} successfully')

@client.command()
@commands.has_permissions(administrator=True)
async def unsubscribe(ctx, act: str) -> None:
    """Unsubs the channel from notifications, needs admin permission"""
    spy(ctx)
    channel = str(ctx.channel.id)
    try:
        file = open(f'{INFO}/{act}.csv', 'r')
        subs = [lines.strip() for lines in file]
        for line in subs:
            for row in line.split(','):
                if channel == row:
                    del(line)
        file = open(f'{INFO}/{act}.csv', 'w')
        for line in subs:
            file.write(f'{line}\n')
            await ctx.send('Channel unsubbed')
    except FileNotFoundError:
        await ctx.send(f'{act} does not exist')

async def activity_changer() -> None:
    """Changes the bot activity
    """ #this is the "status" under the bot name
    #name = f'{PREFIXES}help' #if you want to use a fix activity
    name = choice(open(ACTIVITIES, 'r', encoding='UTF-8').readlines()) #randomly chooses one of the activities in the activities folder
    activity = discord.Activity(name=name, type=discord.ActivityType.watching) #transforms it into the discord class
    #the discord.ActivityType can be other things other than "watching", like: playing, streaming, listening
    await client.change_presence(activity=activity) #makes the change

if __name__ == '__main__':

    os.system('cls||clear') #clear the console for easier visualization

    print('='*50)
    print(f'Welcome to {BOT} bot Ver. {VERSION}') #shows this info on console before booting, not necessary to funcition
    print('='*50)
    sleep(0.5) #waits for half a second, not necessary to function

    os.system('cls||clear')

    for file in os.listdir(COGS): #this loads the cogs/extensions
        if file.endswith('.py'):
            if file.startswith('core') or file.startswith('#'): #core is not a cog and files with # are no implemented
                continue                                        #the choice for # is arbitrary, can be anything
            else:
                client.load_extension(f'cogs.{file[:-3]}') #loads the extensions on "cogs" folder
                print(f'Loading {file[:-3]} extension...') #prints on the console which extension was loaded
                sleep(0.25) #waits for quarter of a second, not necessary to function

    os.system('cls||clear')

    client.run(TOKEN) #runs the bot