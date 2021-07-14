#Modules
import os
import discord
from discord.ext import commands
from time import sleep, localtime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from random import choice
from tqdm import tqdm
from termcolor import cprint

#Constants
BOT = 'Achilles'
VERSION = '0.1.5'
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
    cprint(f'{message}', color='green')
    cprint(f'{localtime()[3]}:{localtime()[4]}:{localtime()[5]}', color='yellow') #hours:mins:secs
    cprint('\nAwaiting command...', color='cyan')

async def activity_changer() -> None: #This is the "status" under the bot name.
    """Changes the bot activity.
    """ 
    name = choice(open(ACTIVITIES, 'r', encoding='UTF-8').readlines()) #Randomly chooses one of the activities in the activities file.
    activity = discord.Activity(name=name, type=discord.ActivityType.watching) #Transforms it into the discord class.
    await client.change_presence(activity=activity)
    status('Changing activity...')

@client.event #Decorator that gives a flag on event.
async def on_ready() -> None: #When the bot is ready for using.
    """Notifies when it's ready and turn on schedulers."""
    status(f'\n{client.user.name} is on')
    await activity_changer()
    scheduler.add_job(activity_changer, CronTrigger(minute=30, second=0)) #Creates a scheduled task, this one changes activity every 30 mins.
    scheduler.start()
    status('Schedulers started')

if __name__ == '__main__': #Makes it can't be run through imports.

    os.system('cls||clear') #Clear the console for easier visualization.

    print('='*50)
    print(f'Welcome to {BOT} bot Ver. {VERSION}')
    print('='*50)
    sleep(0.5)

    os.system('cls||clear')

    for file in tqdm(os.listdir(COGS), desc='Loading cogs', colour='green'):
        #It looks for every file in the cogs folder
        #then checks if it ends with py, if it does loads it
        #if the file starts with # or is the core module it's no implemented.
        if file.endswith('.py'):
            if file.startswith('core') or file.startswith('#'): # # was arbritary it can be anything else or even nothing.
                continue
            else:
                client.load_extension(f'cogs.{file[:-3]}')
                sleep(0.25)

    os.system('cls||clear')

    client.run(TOKEN) #Runs the bot.