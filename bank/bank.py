from typing import NoReturn, Union
import os
from main import BOTDIR

ACCOUNTS = os.path.join(BOTDIR, 'bank/bank_accounts.csv')
INVENTORY = os.path.join(BOTDIR, 'bank/bank_inventory.csv')
#TODO: clear the repetitive readings and writings use only one function call

class Customer:

    def __init__(self, id: str, name: str = '', balance: Union[float, int] = 0.0) -> None:
        if self.read_bank_account(str(id)):
            self.id, self.name, self.balance = self.read_bank_account(str(id))
        else:
            self.id, self.name, self.balance = str(id), name, balance
            self.new_bank_account()
        if not self.read_bank_inventory(str(id)):
            self.new_bank_inventory()

    def _reader(self, path: str, id: str = ''):
        if id == '':
            id = self.id
        with open(path, 'r', encoding='UTF-8') as file:
            raw_data = [line.strip().split(',') for line in file]
        data = [line for line in raw_data if id == line[0]]
        return raw_data, data

    def _writer(self, path: str, data: list):
        with open(path, 'w', encoding='UTF-8') as file:
            for line in data:
                line = ','.join(line)
                file.write(f'{line}\n')

    def read_bank_account(self, id: str = '') -> bool or Union[str, str, str]:
        customer_data = self._reader(ACCOUNTS, id)[1]
        if customer_data == []:
            return False
        id, name, balance = customer_data[0]
        return id, name, balance

    def new_bank_account(self) -> NoReturn:
        with open(ACCOUNTS, 'a', encoding='UTF-8') as file:
            file.write(f'{self.id},{self.name},{self.balance}\n')

    def read_bank_inventory(self, id: str = '') -> bool:
        customer_inventory = self._reader(INVENTORY, id)[1]
        if customer_inventory == []:
            return False
        return customer_inventory

    def new_bank_inventory(self):
        with open(INVENTORY, 'a', encoding='UTF-8') as file:
            file.write(f'{self.id}\n')

    def update_bank_account(self, new_balance: Union[float, int], id: str = '') -> NoReturn:
        raw_data, customer_data = self._reader(ACCOUNTS, id)
        index = raw_data.index(customer_data[0])
        customer_data[0][2] = str(float(new_balance))
        raw_data[index] = customer_data[0]
        self._writer(ACCOUNTS, raw_data)
        self.balance = new_balance

    def add_credit(self, value: Union[int, float]) -> NoReturn:
        new_balance = float(float(self.balance) + float(value))
        self.update_bank_account(new_balance)

    def sub_credit(self, value: Union[int, float], limit: Union[int, float] = 0.0) -> NoReturn:
        new_balance = float(float(self.balance) - float(value))
        if new_balance < limit:
            return ValueError('Operation not authorized, limit exceeded')
        self.update_bank_account(new_balance)

    def add_to_inventory(self, item: str, id: str = ''):
        inventory_data, customer_inventory = self._reader(INVENTORY, id)
        customer_inventory = customer_inventory[1:]
        index = inventory_data.index(customer_inventory[0])
        customer_inventory[0].append(item)
        inventory_data[index] = customer_inventory[0]
        self._writer(INVENTORY, inventory_data)

    def get_balance(self) -> float:
        return float(self.balance)