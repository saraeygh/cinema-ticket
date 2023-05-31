import os
import hashlib
import json
from datetime import datetime
import random
import custom_exceptions


class Client:
    """
    This class is for modeling Clients of our bank database
    """
    FILENAME = "./database/bank_accounts.json"
    clients_info = {}

    def __init__(
        self, national_id: str, first_name: str, last_name: str, accounts: dict = {}
    ):
        if Client.national_id_valid(national_id):
            self.national_id = national_id
        else:
            raise custom_exceptions.InvalidNationalID("Invalid ID.")
        self.first_name = first_name
        self.last_name = last_name
        self.accounts = accounts
        Client.clients_info.update({self.national_id: self.__dict__})

    @staticmethod
    def national_id_valid(national_id: str) -> bool:
        """Checks whether national ID is ten digits.

        Args:
            national_id (str): User inputed National ID.

        Returns:
            Boolean: True if valid & False if invalid.
        """
        if len(national_id) != 10:
            return False
        return True

    def __str__(self) -> str:
        """Cutomize print output of object."""
        return f"""
        National ID: {self.national_id}
        First name: {self.first_name},
        Last name: {self.last_name},
        Bank Accounts: {self.accounts},
        """


class BankAccount:
    """Managing banking affairs

    Raises:
        custom_exceptions.InvalidNationalID: Invalid National ID.
        custom_exceptions.BalanceMinimum: Balance less than required minimum.
    """

    FILENAME = "./database/bank_accounts.json"
    MIN_BALANCE = 10_000
    accounts_dict = {}

    def __init__(
        self,
        national_id: str,
        account_name: str,
        balance: float,
        password: str,
        creation_date: str = None,
        cvv2: int = None,
    ):
        """Initialize instance

        Args:
            national_id (str): User inputed national ID.
            first_name (str): User inputed first name.
            last_name (str): User inputed last name.
            balance (float): User inputed balance.
            password (str): User inputed password.
            creation_date (str): Date and time of bank account creation.
            cvv2 (int): Four digit number as CVV2.

        Raises:
            custom_exceptions.InvalidNationalID: Invalid National ID.
        """
        self.national_id = national_id
        self.account_name = account_name
        self._balance = balance
        self.password = password
        if creation_date is not None:
            self.creation_date = creation_date
        else:
            self.creation_date = datetime.now().isoformat(timespec="seconds")
        if cvv2 is not None:
            self.cvv2 = cvv2
        else:
            self.cvv2 = random.randint(1111, 9999)

        BankAccount.accounts_dict.update({self.account_name: self.__dict__})
        Client.clients_info[self.national_id]["accounts"].update(
            BankAccount.accounts_dict
        )

    @staticmethod
    def create_account(
        national_id: int,
        account_name: str,
        first_name: str,
        last_name: str,
        balance: float,
        password: str,
    ):
        """Create bank account.

        Args:
            national_id (int): User national ID.
            first_name (str): User first name.
            last_name (str): User last name.
            balance (float): User inputed balance.
            password (str): User inputed password.
        """
        if not os.path.exists(BankAccount.FILENAME):
            os.makedirs(os.path.dirname(BankAccount.FILENAME), exist_ok=True)
            BankAccount.json_save(BankAccount.FILENAME, {})

        Client.clients_info = BankAccount.json_import(BankAccount.FILENAME)

        if national_id not in Client.clients_info:
            Client(national_id, first_name, last_name)
            BankAccount(national_id, account_name, balance, password)
            Client.clients_info[national_id]["accounts"].update(
                BankAccount.accounts_dict
            )
            BankAccount.json_save(BankAccount.FILENAME, Client.clients_info)
        elif account_name in Client.clients_info[national_id]["accounts"]:
            raise custom_exceptions.AlreadyExistAccount("Account name already exists.")
        else:
            BankAccount(national_id, account_name, balance, password)
            Client.clients_info[national_id]["accounts"].update(
                BankAccount.accounts_dict
            )
            BankAccount.json_save(BankAccount.FILENAME, Client.clients_info)

    @staticmethod
    def hashing(password: str):
        """
        This method is for hashing passwords
        """
        hashed_pass = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return hashed_pass

    @staticmethod
    def json_save(filename, dictionary):
        """
        This method is use for saving a dictionary into a json file
        """
        with open(filename, mode="w+", encoding="utf-8") as file:
            json.dump(dictionary, file, indent=4)

    @staticmethod
    def json_import(filename) -> dict:
        """
        This method is used for importing data from a json file/
        and assign it to our class dictionary
        """
        with open(filename, mode="r", encoding="utf-8") as file:
            return json.load(file)

    @property
    def balance(self) -> float:
        """Balance Getter

        Returns:
            float: User bank account balance
        """
        return self._balance

    @balance.setter
    def balance(self, balance: int):
        """Balance Setter

        Args:
            balance (int): Inputed balance to deposit.

        Raises:
            custom_exceptions.BalanceMinimum: If balance goes down the min limit.
        """
        if balance < BankAccount.MIN_BALANCE:
            raise custom_exceptions.BalanceMinimum("Invalid balance.")
        self._balance = balance

    @staticmethod
    def password_check(password: str) -> bool:
        if len(password) < 4:
            return False
        return True

    @property
    def password(self) -> str:
        """Password Getter

        Returns:
            str: Password as string.
        """
        return self.__password

    @password.setter
    def password(self, password: str):
        """Password Setter

        Args:
            password (str): Inputed password.
        """
        if not BankAccount.password_check(password):
            raise custom_exceptions.ShortPasswordError("Too short Password!")
        password = BankAccount.hashing(password)
        self.__password = password

    @staticmethod
    def deposit(national_id, account_name, password, cvv2, amount: int):
        """Deposit method

        Args:
            amount (int): Amount to deposit.

        Raises:
            custom_exceptions.BalanceMinimum: If balance goes down the min limit.
        """
        accounts_info = BankAccount.json_import(BankAccount.FILENAME)

        if national_id not in accounts_info:
            raise custom_exceptions.UnsuccessfulDeposit(
                "Unsuccessful deposit, national ID not found."
            )

        if account_name not in accounts_info[national_id]["accounts"]:
            raise custom_exceptions.UnsuccessfulDeposit(
                "Unsuccessful deposit, No such account."
            )

        if (
            BankAccount.hashing(password)
            != accounts_info[national_id]["accounts"][account_name][
                "_BankAccount__password"
            ]
        ):
            raise custom_exceptions.UnsuccessfulDeposit(
                "Unsuccessful deposit, Wrong password."
            )

        if cvv2 != accounts_info[national_id]["accounts"][account_name]["cvv2"]:
            raise custom_exceptions.UnsuccessfulDeposit(
                "Unsuccessful deposit, Wrong CVV2."
            )

        if (
            accounts_info[national_id]["accounts"][account_name]["_balance"] + amount
            < BankAccount.MIN_BALANCE
        ):
            raise custom_exceptions.BalanceMinimum("Invalid balance.")

        accounts_info[national_id]["accounts"][account_name]["_balance"] += amount
        BankAccount.json_save(BankAccount.FILENAME, accounts_info)

    @staticmethod
    def withdraw(national_id, account_name, password, cvv2, amount: int):
        """Withdraw method

        Args:
            amount (int): Amount to withdraw.

        Raises:
            custom_exceptions.BalanceMinimum: If balance goes down the min limit.
        """
        accounts_info = BankAccount.json_import(BankAccount.FILENAME)

        if national_id not in accounts_info:
            raise custom_exceptions.UnsuccessfulIdDeposit(
                "Unsuccessful deposit, national ID not found."
            )

        if account_name not in accounts_info[national_id]["accounts"]:
            raise custom_exceptions.UnsuccessfulAccountDeposit(
                "Unsuccessful deposit, No such account."
            )

        if (
            BankAccount.hashing(password)
            != accounts_info[national_id]["accounts"][account_name][
                "_BankAccount__password"
            ]
        ):
            raise custom_exceptions.UnsuccessfulPasswordDeposit(
                "Unsuccessful deposit, Wrong password."
            )

        if cvv2 != accounts_info[national_id]["accounts"][account_name]["cvv2"]:
            raise custom_exceptions.UnsuccessfulCvv2Deposit(
                "Unsuccessful deposit, Wrong CVV2."
            )

        if (
            accounts_info[national_id]["accounts"][account_name]["_balance"] - amount
            < BankAccount.MIN_BALANCE
        ):
            raise custom_exceptions.BalanceMinimum("Invalid balance.")

        accounts_info[national_id]["accounts"][account_name]["_balance"] -= amount
        BankAccount.json_save(BankAccount.FILENAME, accounts_info)

    def __str__(self) -> str:
        """Cutomize print output of object."""
        return f"""
        National ID: {self.national_id}
        Account Name: {self.account_name},
        Balance: {self._balance},
        creation_date: {self.creation_date},
        cvv2: {self.cvv2}
        """


def main():
    pass


if __name__ == "__main__":
    main()
