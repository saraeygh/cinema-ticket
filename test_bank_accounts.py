#! /usr/bin/python3

import unittest
from bank_accounts import BankAccount
from custom_exceptions import BalanceMinimum
from human import Human

FILENAME = "./database/bank_accounts.json"
class TestBankAccount(unittest.TestCase):

    def test_national_id_valid(self):
        pass

    def test_deposit(self):
        pass
    
    def test_withdraw(self):
        pass
    
def main():
    """
    This is our main module function
    """
    unittest.main()

if __name__ == "__main__":
    main()
