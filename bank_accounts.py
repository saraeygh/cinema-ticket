from os import path
import random
import custom_exceptions
import human
from datetime import datetime
from os import path


class BankAccount():
    
    MIN_BALANCE = 10_000
    accounts_dict = {}
    
    def __init__(self,
                 national_id: str,
                 first_name: str,
                 last_name: str,
                 balance: float,
                 password: str,
                 creation_date: str = None,
                 cvv2: int = None):
        if BankAccount.national_id_valid(national_id):
            self.national_id = national_id
        else:
            raise ValueError("Invalid ID.")
        self.first_name = first_name
        self.last_name = last_name
        self._balance = balance
        self._password = human.Human.hashing(password)
        if creation_date == None:
            self.creation_date = str(datetime.now())
        else:
            self.creation_date = creation_date
        if cvv2 == None:
            self.cvv2 = random.randint(1111,9999)
        else:
            self.cvv2 = cvv2

    @staticmethod
    def national_id_valid(national_id: str):
        if len(national_id) < 10:
            return False
        return True

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance:int):
        if balance < 10_000:
            raise ValueError('Invalid balance.')
        self._balance = balance
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password: str):
        self._password = password

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

    @staticmethod
    def create_account(national_id: int,
                       first_name: str,
                       last_name: str,
                       balance: float,
                       password: str,
                       ):
        new_account = BankAccount(national_id, first_name, last_name, balance, password)
        BankAccount.accounts_dict.update({new_account.national_id: new_account.__dict__})
        human.Human.json_save("bank_accounts.json", BankAccount.accounts_dict)

    def __str__(self) -> str:
        return f"""
        National ID: {self.national_id}
        Name: {self.first_name},
        Last: {self.last_name},
        Balance: {self._balance},
        Password: {self._password},
        creation_date: {self.creation_date},
        cvv2: {self.cvv2}
        """
    

# acc1 = BankAccount.create_account("2210240344", "reza", "saraey", 10_000, "1234")
# acc2 = BankAccount.create_account("22100", "matin", "ghane", 100_000, "4315")
# #acc3 = BankAccount("22100", "matin", "ghane", 100_000, "4315")
# acc4 = BankAccount.create_account("2210083419", "matin", "ghane", 100_000, "4315")