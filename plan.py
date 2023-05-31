"""
This module contains Plan, Silver and Glod classes/
for modeling various types of user plan
"""
from abc import ABC
from human import User
import custom_exceptions
from bank_accounts import BankAccount
from datetime import datetime

USERS_JSON = "./database/users.json"

class Silver(ABC):

    PRICE = 10_000
    DISCOUNT = 0.2

    def __init__ (self):
        pass

    def active(self, username, national_id, account_name, password, cvv2):
        if BankAccount.withdraw(national_id, account_name, password, cvv2, Silver.PRICE):
            credit = 3
            users_data = BankAccount.json_import(USERS_JSON)
            users_data[username].update({"credit": credit})
            User.change_plan(self, username, "Silver")
        else:
            raise custom_exceptions.BuySilverFailed("Payment failed, Couldnt activate silver plan.")

    def deactive(self, username):
        User.change_plan(self, username, "Bronze")

    def use_plan(self, username, cost, national_id, account_name, password, cvv2):

        users_data = BankAccount.json_import(USERS_JSON)

        if users_data[username]["credit"] == 0:
            Silver.deactive(self, username)
            return False
        else:
            discount_cost = (cost * (1 - Silver.DISCOUNT))
            if BankAccount.withdraw(national_id, account_name, password, cvv2, discount_cost):
                users_data[username]["credit"] -= 1
                users_data[username]["wallet"] += (Silver.DISCOUNT * cost)
                BankAccount.json_save(USERS_JSON, users_data)
            
class Gold(ABC):

    PRICE = 50_000
    DISCOUNT = 0.5

    def __init__(self):
        pass
 
    def active(self, username, national_id, account_name, password, cvv2):
        if BankAccount.withdraw(national_id, account_name, password, cvv2, Gold.PRICE):
            buy_date_time = datetime.now()
            users_data = BankAccount.json_import(USERS_JSON)
            users_data[username].update({"credit": credit})
            User.change_plan(self, username, "Silver")
        else:
            raise custom_exceptions.BuySilverFailed("Payment failed, Couldnt activate silver plan.")

    def deactive(self, username):
        User.change_plan(self, username, "Bronze")

    def use_plan(self, username, cost, national_id, account_name, password, cvv2):

        users_data = BankAccount.json_import(USERS_JSON)

        if users_data[username]["credit"] == 0:
            Silver.deactive(self, username)
            return False
        else:
            discount_cost = (cost * (1 - Silver.DISCOUNT))
            if BankAccount.withdraw(national_id, account_name, password, cvv2, discount_cost):
                users_data[username]["credit"] -= 1
                users_data[username]["wallet"] += (Silver.DISCOUNT * cost)
                BankAccount.json_save(USERS_JSON, users_data)