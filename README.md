![Achilles and Zagreus](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/0b3d3fe1-90de-4fc6-91b5-c43cc6b8af5e/debqth5-85549e2b-5684-4196-b0e2-3058ffc84a82.jpg/v1/fill/w_852,h_938,q_70,strp/achilles_and_baby_zagreus_by_cathiane_debqth5-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTQxMCIsInBhdGgiOiJcL2ZcLzBiM2QzZmUxLTkwZGUtNGZjNi05MWI1LWM0M2NjNmI4YWY1ZVwvZGVicXRoNS04NTU0OWUyYi01Njg0LTQxOTYtYjBlMi0zMDU4ZmZjODRhODIuanBnIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.8w6VY5Oaw2W4zJIDe_b5maZy8tR6iRFyBHvWnyuo_jo)
##### Incredible art by: [Cathiane](https://www.deviantart.com/cathiane)
# <b>AchillesBot</b>
## <b>About</b>
 A Discord bot that intends to help others create and customize their own bot. Previous programming languages knowledge, especially Python, is required to fully understand the bot programming, altough I really try to explain everything. The bot is under the MIT License, so feel free to fork it or make your own bot using this as basis!
### <b>Personality</b>
<i><b>Achilles</b> is named after the character from [<b>Supergiant Games</b>](https://www.supergiantgames.com) awesome game [<b>Hades</b>](https://www.supergiantgames.com/games/hades). He's the <b>mentor</b> of Zagreus and as this bot is meant to <b>teach</b> people or at least serve as a template to other bots, so it felt pretty fit to the personality!</i>

---
## <b>Dependencies</b>
To use this bot we first need to install some dependencies. If you are on Windows just open command prompt or PowerShell and type the command.

First install [discord.py](https://discordpy.readthedocs.io/en/stable/) :
```cmd
pip install discord
```

For scheduled tasks we are using [apscheduler](https://apscheduler.readthedocs.io/en/stable/) :
```cmd
pip install apscheduler
```

Just for looks we are using [tqdm](https://pypi.org/project/tqdm/) and [termcolor](https://pypi.org/project/termcolor/):
```cmd
pip install tqdm
pip install termcolor
```

---
## <b>How to use</b>
The bot <b>functions by just running the <i>main.py</i> file</b>, but first you have to setup two infos in the <i>botinfo.txt</i> under the infos folder.

### <b>Token</b>
You just need to put the bot's token in the first line!

### <b>Prefixes</b>
You need to choose wich prefixes will be available for the commands to be called, you need at least one, if using more separate then by commas and no spaces.

### The botinfo file should be as
```txt
BOT TOKEN HERE
+,>,$
```
As soon these are filled <b>just run the bot!</b>

---
## If you are reading this ...
Hello! As of this release this isn't a lot in yet, it does work tough! There still a lot of things to implement and more to explain. Soon enough this README will show you how to create the bot in the Discord site and how to get the TOKEN to run the bot, for now I'm sorry for being incomplete, but I hope it helps someway.