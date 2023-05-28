from os import path
import random
import custom_exceptions

if path.exists("./database.json"):
    User.dictionary = User.json_import()
else:
    User.json_create()

class BankAccount():
    
    MIN_BALANCE = 10_000
    
    def __init__(self, 
                 first_name: str,
                 last_name: str,
                 balance: float,
                 creation_date: str,
                 password: str,
                 cvv2: int):
        
        self.first_name = first_name
        self.last_name = last_name
        self._balance = balance
        self.creation_date = creation_date
        self._password = password
        self._cvv2 = cvv2

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance:int):
        if balance < 10_000:
            raise ValueError('Invalid balance.')
        self._balance = balance
    
    @property
    def _password(self):
        return self._password
    
    @_password.setter
    def _password(self):
        pass

    def deposit(self, amount: int):
        if self._balance + amount < self.MIN_BALANCE:
            raise ValueError('Invalid balance.')
        self._balance += amount

    def withdraw(self, amount: int):
        if self._balance - amount < self.MIN_BALANCE:
            raise ValueError('Invalid balance.')
        self._balance -= amount

    def transfer(self, other, amount: int):
        self.withdraw(amount)
        other.deposit(amount)

    def create_account(self,
                       first_name: str,
                       last_name: str,
                       balance: float,
                       creation_date: str,
                       password: str,
                       cvv2: int
                       ):
        
        number = random.randit(0000,9999)