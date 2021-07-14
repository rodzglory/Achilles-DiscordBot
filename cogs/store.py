from typing import Optional, Union
import discord
from discord.ext import commands
from .core import Core
from bank.bank import Customer
from main import status, TEXTS
import os
#TODO: credits
#TODO: buy
#TODO: sell
#TODO: auction Discord only?
#TODO: bets Discord only?

ITEMS = os.path.join(TEXTS, 'items.csv')
CREDITS = 'credits'

class Store(Core):

    def __init__(self, client) -> None:
        super().__init__(client)

    @commands.command()
    async def balance(self, ctx) -> float:
        """Shows your account balance"""
        mention, locale, id = self.spy(ctx)
        customer = Customer(id)
        balance = customer.get_balance()
        del customer
        status('Showing balance...')
        
        embed = await self.embed(title=id, description=balance, thumbnail=ctx.author.avatar_url, color=ctx.author.color)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item: Optional[str] = None):
        """Buys one of the items... if you have the money"""
        id = self.spy(ctx)[2]
        if item != None:
            item = item.lower()
        else:
            return await ctx.send(f'You need to specify the item you want to buy')
        with open(ITEMS, 'r', encoding='UTF-8') as file:
            items_data = [line.strip().split(',') for line in file]
            items = [line[0] for line in items_data[1:]]
        if item not in items:
            return await ctx.send(f'There\'s no {item} available to purchase')
        else:
            item_data = [data for data in items_data if item == data[0]]
            if float(item_data[0][2]) < 1:
                return await ctx.send(f'There\'s no stock of {item} available')
            else:
                try: #TODO: subtract from items :)
                    customer = Customer(id)
                    value = float(customer.get_balance() - float(item_data[0][2]))
                    customer.sub_credit(value)
                    customer.add_to_inventory(item)
                    del customer
                    status('Buying...')
                    await ctx.send(f'{item} was bought')
                except ValueError:
                    return await ctx.send(f'You have no {CREDITS} left')

def setup(client):
    client.add_cog(Store(client))