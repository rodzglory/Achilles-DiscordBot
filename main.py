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
VERSION = '0.1.0' #bot version
FOOTER = 'Achilles Bot' #footer for embed
AUDIO = os.path.join(BOTDIR, 'audio') #audios folder
SAMPLE = os.path.join(AUDIO, 'sample') #shortes audios folder

client = commands.Bot(command_prefix=PREFIXES) #calls the bot object, the most important thing to make the bot work
scheduler = AsyncIOScheduler() #scheduler for automated tasks

def status(message: str = 'Probably forgot the status...') -> print: #this function is not necessary for the bot to work
    """Changes the console status
    """
    print(f'{message} {localtime()[3]}:{localtime()[4]}:{localtime()[5]}') #prints a defined message and the time like hour:mins:secs
    print('\nAwaiting command...') #prints thats it's ready for other command

def spy(ctx) -> Union(str, str): #this function is not necessary for the bot to work
    """Save information from new users of the bot and returns their mention code and locale
    """
    id = ctx.author.id #gets the id from the person that used the command
    name = ctx.author.name #gets the name from the person that used the command
    mention = ctx.author.mention #gets the mention code from the person that used the command
    data = [str(id), str(name), str(mention)] #prepares the info above to be saved in a csv file
    data = ','.join(data) #make it into a string
    locale = ctx.guild.preferred_locale #gets the preferred locale of the guild
    users = [lines.strip() for lines in open(USERS)] #reads the file so that we don't have copys of users
    for line in users: #searches in all of lines from the csv
        for column in line.split(','): #searches in all rows from the line
        #another way of doing this is `if line.split(',')[0] == str(id):` would substitute both the line up and the line down
            if str(id) == column: #the user id is unique so we just verify if it's already in the csv
                return mention, locale
    else:
        open(USERS, 'a').write(f'{data}\n') #if it isn't we save it
        status('New user registered')
        return mention, locale

async def activity_changer() -> None: #this is the "status" under the bot name
    """Changes the bot activity
    """ 
    #name = f'{PREFIXES}help' #if you want to use a fix activity
    name = choice(open(ACTIVITIES, 'r', encoding='UTF-8').readlines()) #randomly chooses one of the activities in the activities folder
    activity = discord.Activity(name=name, type=discord.ActivityType.watching) #transforms it into the discord class
    #the discord.ActivityType can be other things other than "watching", like: playing, streaming, listening
    await client.change_presence(activity=activity) #makes the change

@client.event #decorator that gives a flag on event
async def on_ready() -> None: #when the bot is ready for using do:
    """Notifies when it's ready and turn on schedulers"""
    status(f'\n{client.user.name} is on')
    await activity_changer() #changes the bot's activity/status
    #schedulers on ready
    scheduler.add_job(activity_changer, CronTrigger(minute=30, second=0)) #creates a scheduled task, this one changes activity every 30 mins
    scheduler.start() #starts all tasks under the scheduler object
    status('Schedulers started')

@client.command(hidden=True) #this is a Discord command, won't show on the help command
@commands.has_permissions(administrator=True) #checks if the user that called it has the permission administrator
async def reload(ctx, extension) -> None: #ctx (context) parameter gets the message object
    """Reloads a cog"""
    spy(ctx)
    client.reload_extension(f'cogs.{extension}')
    status(f'Reloading {extension}...')
    await ctx.send(f'{extension} reloaded') #the bot sends a message to the same text channel it was called

@client.command(hidden=True)
@commands.has_permissions(administrator=True) #if you don't want to limit who has access to the command just remove the line
async def load(ctx, extension) -> None:
    """Loads an unloaded cog"""
    spy(ctx)
    client.load_extension(f'cogs.{extension}')
    status(f'Loading {extension}...')
    await ctx.send(f'{extension} loaded')

@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def unload(ctx, extension) -> None:
    """Unloads a loaded cog"""
    spy(ctx)
    client.unload_extension(f'cogs.{extension}')
    status(f'Unloading {extension}...')
    await ctx.send(f'{extension} unloaded')

@client.command(aliases=['clear'])
@commands.has_permissions(manage_messages=True) #the bot needs this permission as well, I don't recommend removing this check, because anyone could just clear all the server messages
async def purge(ctx, amt=100) -> None:
    """Clears channel of an amount (default 100) of messages, needs manage messages permission"""
    spy(ctx)
    await ctx.channel.purge(limit = amt + 1) #this makes the bot clear messages
    await ctx.send(f'The last {amt} messages were purged')
    status(f'Purging {amt}...')

@client.command()
@commands.has_permissions(administrator=True)
async def subscribe(ctx, act: str) -> None: #the act (activity) parameter is the name of csv file containing info from the channel
    """Subscribes the channel to notifications, needs admin permission"""
    spy(ctx)
    channel = str(ctx.channel.id) #gets the id of the channel where the command was used
    name = str(ctx.channel.name) #gets the name of the channel where the command was used
    guild = str(ctx.channel.guild) #gets the guild name from the channel where the command was used
    data = [channel, name, guild]
    data = ','.join(data)
    try:
        file = open(f'{INFO}/{act}.csv')
        subs = [lines.strip() for lines in file]
        for line in subs:
            for row in line.split(','):
                if channel == row: #if channel is already subscribed in the told activity
                    await ctx.send('Channel already subscribed')
                    return status('Oops')
        else: #if it's not, it will save it
            open(f'{INFO}/{act}.csv', 'a', encoding='UTF-8').write(f'{data}\n')
            status(f'Subscribing {name} to {act}, from {guild}')
            await ctx.send(f'Channel {name} subscribed to {act} successfully')
    except FileNotFoundError: #if the activity does not exist creates a new csv with it
        file = open(f'{INFO}/{act}.csv', 'w', encoding='UTF-8').write(f'id,name,guild\n{data}\n')
        status(f'Subscribing {name} to {act}, from {guild}')
        await ctx.send(f'Channel {name} subscribed to {act} successfully')

@client.command()
@commands.has_permissions(administrator=True)
async def unsubscribe(ctx, act: str) -> None: #reverse from subscribe ;)
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

if __name__ == '__main__': #the bot only runs if this is the file being run, makes it cannot be run through imports

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