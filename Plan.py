#!/usr/bin/python3

from human import User
from datetime import datetime, timedelta
from bank_accounts import BankAccount

class Plan():
   def __init__(self, username):
       self.username = username


# Define user-active mode function
   def active(self, username):
       pass


# Define user-deactive mode function
   def deactive(self, username):
       pass


# Definition of discount part function
   def use_plan(self, username):
       pass


class Silver(Plan):
   
   PRICE = 100_000
   DISCOUNT = 0.2

   def __init__ (self):
       super().__init__(self)
       
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
          return (cost * (1 - Silver.DISCOUNT))
      
   def __str__(self):
       # get user_credit from json
       return f"Remanied count: {self.user_credit}"
   

class Gold(Plan):

   PRICE = 500_000
   DISCOUNT = 0.5

   def __init__(self, username):
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
      else:
          return (cost * (1 - Gold.DISCOUNT)), "Energy drink"

   def __str__(self):
         return f"remanied count: {self.count}"
