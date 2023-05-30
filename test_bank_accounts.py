#! /usr/bin/python3

import unittest
from bank_accounts import BankAccount
from custom_exceptions import BalanceMinimum
from human import Human


class TestBankAccount(unittest.TestCase):

    def test_national_id_valid(self):
        valid_id = "2210010098"
        invalid_id = "221001098"
        self.assertTrue(BankAccount.national_id_valid(valid_id))
        self.assertFalse(BankAccount.national_id_valid(invalid_id))

    def test_deposit(self):
        account1 = BankAccount("2210000344", "Reza", "Saraey", 100_000, "1234")
        deposit_amount = 50_000
        account1.deposit(account1.national_id  , deposit_amount)
        self.assertEqual(account1.balance, 150_000)
        
        account2 = BankAccount("2210000344", "Reza", "Saraey", 50_000, "1234")
        deposit_amount = -45_000
        with self.assertRaises(BalanceMinimum):
            account2.deposit(deposit_amount)

    def test_withdraw(self):
        account1 = BankAccount("2210000344", "Reza", "Saraey", 100_000, "1234")
        withdraw_amount = 50_000
        account1.withdraw(withdraw_amount)
        self.assertEqual(account1.balance, 50_000)
        
        account2 = BankAccount("2210000344", "Reza", "Saraey", 50_000, "1234")
        withdraw_amount = 45_000
        with self.assertRaises(BalanceMinimum):
            account2.withdraw(withdraw_amount)

    def test_create_account(self):
        BankAccount.create_account("2210240300", "reza", "saraey", 10_000, "1234")
        data = Human.json_import("./database/bank_accounts.json")
        print(data["2210240300"])
        self.assertEqual(data["2210240300"]["national_id"], "2210240300")
        self.assertEqual(data["2210240300"]["first_name"], "reza")
        self.assertEqual(data["2210240300"]["last_name"], "saraey")
        self.assertEqual(data["2210240300"]["_balance"], 10_000)

def main():
    """
    This is our main module function
    """
    unittest.main()


if __name__ == "__main__":
    main()
