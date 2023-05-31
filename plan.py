"""
This module contains Plan, Silver and Glod classes/
for modeling various types of user plan
"""
from abc import ABC, abstractmethod
from human import User
import datetime
from bank_accounts import BankAccount

class Plan(ABC):
    def __init__(self, username, record_date):
        self.username = username
        self.record_date = record_date

# Define user-active mode function
    @abstractmethod
    def active(self, username):
        pass

# Define user-deactive mode function
    @abstractmethod
    def deactive(self, username):
        pass

# Definition of discount part function
    @abstractmethod
    def use_plan(self, username):
        pass

    def __str__(self):
        pass


class Silver(Plan):

    PRICE = 100_000
    DISCOUNT = 0.2

    def __init__ (self, username, record_date, credit):
        super().__init__(username, record_date)

    def active(self, username):
        User.change_plan(self, username, "Silver")
        credit = 3
        # Save credit in user json.
        BankAccount.withdraw(self, Silver.PRICE)

    def deactive(self, username):
        User.change_plan(self, username, "Bronze")

    @classmethod
    def use_plan(self, username, cost, user_credit):
        if user_credit == 0:
            print("you have no credit.")
            Silver.deactive(self, username)
        else:
            user_credit -= 1
            return cost * (1 - Silver.DISCOUNT)
    User.charge_wallet += PRICE * DISCOUNT

    def __str__(self):
        # get user_credit from json
        return f"Remanied count: {self.user_credit}"


class Gold(Plan):

    PRICE = 500_000
    DISCOUNT = 0.5

    def __init__(self, username, record_date, credit):
        super().__init__(username)
 
    def active(self, username):
        User.change_plan(self, username, "Gold")
        start_date = datetime.now()
        expire_date = start_date + timedelta(days=30)
        # Save to json
 
    def deactive(self, username):
        User.change_plan(self, username, "Bronze")
    
    def use_plan(self, username, cost):
        # exipre_date = Load user info from json
        if datetime.now() >  expire_date:
            print("Your gold plan expired.")
            Gold.deactive()
        else:
            return (cost * (1 - Gold.DISCOUNT)), "Energy drink"
            BankAccount.withdraw(self, Gold.PRICE)

    def __str__(self):
        return f"remanied expire_date: {self.user_credit}"
