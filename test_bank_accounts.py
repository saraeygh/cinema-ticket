#! /usr/bin/python3

import unittest
from bank_accounts import BankAccount, Client
import custom_exceptions
from human import Human

FILENAME = "./database/bank_accounts.json"

class TestClient(unittest.TestCase):
    
    def test_national_id_valid(self):
        valid_id = "9876543210"
        invalid_id = "987654321"
        self.assertTrue(Client.national_id_valid(valid_id))
        self.assertFalse(Client.national_id_valid(invalid_id))


class TestBankAccount(unittest.TestCase):

    def test_create_account(self):
        national_id = "0123456789"
        account_name = "melli"
        fname = "reza"
        lname = "saraey"
        balance = 50_000
        password = "1234"
        BankAccount.create_account(national_id, account_name, fname, lname, balance, password)
        new_account = BankAccount.json_import(FILENAME)
        self.assertEqual(new_account["0123456789"]["national_id"], "0123456789")
        self.assertEqual(new_account["0123456789"]["first_name"], "reza")
        self.assertEqual(new_account["0123456789"]["last_name"], "saraey")
        self.assertEqual(new_account["0123456789"]["accounts"]["melli"]["account_name"], "melli")
        self.assertEqual(new_account["0123456789"]["accounts"]["melli"]["_balance"], 50_000)
        
        with self.assertRaises(custom_exceptions.AlreadyExistAccount):
            BankAccount.create_account(national_id, account_name, fname, lname, balance, password)

        pass1 = BankAccount.hashing("1234")
        pass2 = BankAccount.hashing("1234")
        self.assertEqual(pass1, pass2)

    def test_deposit(self):
        national_id = "0123456789"
        account_name = "melli"
        password = "1234"
        deposit_amount = 50_000
        accounts = BankAccount.json_import(FILENAME)
        cvv2 = accounts[national_id]["accounts"][account_name]["cvv2"]
        BankAccount.deposit(national_id, account_name, password, cvv2, deposit_amount)
        accounts = BankAccount.json_import(FILENAME)
        self.assertEqual(accounts[national_id]["accounts"][account_name]["_balance"], 100_000)
        
        with self.assertRaises(custom_exceptions.UnsuccessfulDeposit):
            BankAccount.deposit((national_id.replace("0", "1")), account_name, password, cvv2, deposit_amount)

        with self.assertRaises(custom_exceptions.UnsuccessfulDeposit):
            BankAccount.deposit(national_id, ("A"+account_name), password, cvv2, deposit_amount)

        with self.assertRaises(custom_exceptions.UnsuccessfulDeposit):
            BankAccount.deposit(national_id, account_name, ("1"+password), cvv2, deposit_amount)

        with self.assertRaises(custom_exceptions.UnsuccessfulDeposit):
            BankAccount.deposit(national_id, account_name, password, (cvv2+1), deposit_amount)

        with self.assertRaises(custom_exceptions.BalanceMinimum):
            BankAccount.deposit(national_id, account_name, password, cvv2, -110_000)

    
    def test_withdraw(self):
        national_id = "0123456789"
        account_name = "melli"
        password = "1234"
        withdraw_amount = 50_000
        accounts = BankAccount.json_import(FILENAME)
        cvv2 = accounts[national_id]["accounts"][account_name]["cvv2"]
        BankAccount.withdraw(national_id, account_name, password, cvv2, withdraw_amount)
        accounts = BankAccount.json_import(FILENAME)
        self.assertEqual(accounts[national_id]["accounts"][account_name]["_balance"], 50_000)

        with self.assertRaises(custom_exceptions.UnsuccessfulDeposit):
            BankAccount.withdraw((national_id.replace("0", "1")), account_name, password, cvv2, withdraw_amount)

        with self.assertRaises(custom_exceptions.UnsuccessfulDeposit):
            BankAccount.withdraw(national_id, ("A"+account_name), password, cvv2, withdraw_amount)

        with self.assertRaises(custom_exceptions.UnsuccessfulDeposit):
            BankAccount.withdraw(national_id, account_name, ("1"+password), cvv2, withdraw_amount)

        with self.assertRaises(custom_exceptions.UnsuccessfulDeposit):
            BankAccount.withdraw(national_id, account_name, password, (cvv2+1), withdraw_amount)

        with self.assertRaises(custom_exceptions.BalanceMinimum):
            BankAccount.withdraw(national_id, account_name, password, cvv2, 110_000)
    
def main():
    """
    This is our main module function
    """
    unittest.main()

if __name__ == "__main__":
    main()
