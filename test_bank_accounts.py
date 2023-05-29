#! /usr/bin/python3

import unittest
import os
import shutil
import pathlib
from bank_accounts import BankAccount
from custom_exceptions import BalanceMinimum


class TestBankAccount(unittest.TestCase):
    
 
    def test_national_id_valid(self) -> bool:
        valid_id = "2210010098"
        invalid_id = "221001098"
        self.assertEqual(BankAccount.national_id_valid(valid_id), True)
        self.assertEqual(BankAccount.national_id_valid(invalid_id), False)

    def test_deposit(self):
        account1 = BankAccount("2210000344", "Reza", "Saraey", 100_000, "1234")
        deposit_amount = 50_000
        account1.deposit(deposit_amount)
        self.assertEqual(account1.balance, 150_000)
        
        account2 = BankAccount("2210000344", "Reza", "Saraey", 50_000, "1234")
        deposit_amount = -45_000
        self.assertRaises(account2.deposit(deposit_amount), BalanceMinimum)
        
        
        # if self._balance + amount < self.MIN_BALANCE:
        #     raise custom_exceptions.BalanceMinimum("Invalid balance.")
        # self._balance += amount


def main():
    """
    This is our main module function
    """
    unittest.main()


if __name__ == "__main__":
    main()
