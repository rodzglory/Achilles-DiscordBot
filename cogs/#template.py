from discord.ext import commands
from main import TEXTS

class Test(commands.Cog):
    
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Test(client))