import os
import hashlib
import json
import logging
import platform
from datetime import datetime
import random
import custom_exceptions

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")

os.makedirs(os.path.dirname("./log/bank_accounts.log"), exist_ok=True)
file_handler = logging.FileHandler("./log/bank_accounts.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

"""
Imported random to generate CVV2.
Imported custom_exceptions to customize raised exceptions.
Imported human module to use its methods.
Imported datetime module to capture account creation timestamp.
"""

class BankAccount:
    """Managing banking affairs

    Raises:
        custom_exceptions.InvalidNationalID: Invalid National ID.
        custom_exceptions.BalanceMinimum: Balance less than required minimum.
    """
    FILENAME = "./database/bank_accounts.json"
    MIN_BALANCE = 10_000
    accounts_info = {}
    def __init__(
        self,
        national_id: str,
        account_name: str,
        first_name: str,
        last_name: str,
        balance: float,
        password: str,
        creation_date: str = None,
        cvv2: int = None,
        accounts: dict = {}
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
        if BankAccount.national_id_valid(national_id):
            self.national_id = national_id
            logger.debug(f"{self.national_id} was valid.")
        else:
            logger.debug(f"{national_id} was not valid.")
            raise custom_exceptions.InvalidNationalID("Invalid ID.")
        self.account_name = account_name
        self.first_name = first_name
        self.last_name = last_name
        self._balance = balance
        self.accounts = accounts
        self.password = password
        if creation_date is not None:
            self.creation_date = creation_date
        else:
            self.creation_date = datetime.now().isoformat(timespec="seconds")
        if cvv2 is not None:
            self.cvv2 = cvv2
        else:
            self.cvv2 = random.randint(1111, 9999)
        self.accounts.update({self.account_name: self.__dict__})
        BankAccount.accounts_info.update({self.national_id: self.accounts})

    @staticmethod
    def hashing(password: str):
        """
        This method is for hashing passwords
        """
        hashed_pass = (hashlib.sha256(password.encode("utf-8")).hexdigest())
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
            logger.debug(f"Balance can not be less that Minimum {BankAccount.MIN_BALANCE}.")
            raise custom_exceptions.BalanceMinimum("Invalid balance.")
        logger.debug(f"Set balance = {self._balance} for national ID {self.national_id}")
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
            logger.debug(f"Password was short and not changed for national ID {self.national_id}")
            raise custom_exceptions.ShortPasswordError("Too short Password!")
        logger.debug(f"Password changed for national ID {self.national_id}")
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
            logger.debug(f"Unsuccessful deposit, {national_id} not found.")
            raise custom_exceptions.UnsuccessfulDeposit("Unsuccessful deposit, national ID not found.")

        if account_name not in accounts_info[national_id]:
            logger.debug(f"Unsuccessful deposit, No such account.")
            raise custom_exceptions.UnsuccessfulDeposit("Unsuccessful deposit, No such account.")

        if BankAccount.hashing(password) != accounts_info[national_id][account_name]["_BankAccount__password"]:
            logger.debug(f"Unsuccessful deposit, Wrong password.")
            raise custom_exceptions.UnsuccessfulDeposit("Unsuccessful deposit, Wrong password.")

        if cvv2 != accounts_info[national_id][account_name]["cvv2"]:
            logger.debug(f"Unsuccessful deposit, {cvv2} for CVV2 is wrong.")
            raise custom_exceptions.UnsuccessfulDeposit("Unsuccessful deposit, Wrong CVV2.")

        if accounts_info[national_id][account_name]["_balance"] + amount < BankAccount.MIN_BALANCE:
            logger.debug(f"Unsuccessful deposit, Balance cant be less than {BankAccount.MIN_BALANCE}.")
            raise custom_exceptions.BalanceMinimum("Invalid balance.")

        logger.debug(f"Successfully deposited {amount} to {national_id}-{account_name} bank account.")
        accounts_info[national_id][account_name]["_balance"] += amount
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
            logger.debug(f"Unsuccessful withdraw, {national_id} not found.")
            raise custom_exceptions.UnsuccessfulWithdraw("Unsuccessful withdraw, national ID not found.")
        if account_name not in accounts_info[national_id]:
            logger.debug(f"Unsuccessful deposit, No such account.")
            raise custom_exceptions.UnsuccessfulDeposit("Unsuccessful deposit, No such account.")
        if BankAccount.hashing(password) != accounts_info[national_id][account_name]["_BankAccount__password"]:
            logger.debug(f"Unsuccessful withdraw, Wrong password.")
            raise custom_exceptions.UnsuccessfulWithdraw("Unsuccessful withdraw, Wrong password.")
        if cvv2 != accounts_info[national_id][account_name]["cvv2"]:
            logger.debug(f"Unsuccessful Withdraw, {cvv2} for CVV2 is wrong.")
            raise custom_exceptions.UnsuccessfulWithdraw("Unsuccessful Withdraw, Wrong CVV2.")
        if accounts_info[national_id][account_name]["_balance"] - amount < BankAccount.MIN_BALANCE:
            logger.debug(f"Unsuccessful Withdraw, Balance cant be less than {BankAccount.MIN_BALANCE}.")
            raise custom_exceptions.BalanceMinimum("Invalid balance.")

        logger.debug(f"Successfully Withdrawed {amount} from {national_id}-{account_name} bank account.")
        accounts_info[national_id][account_name]["_balance"] -= amount
        BankAccount.json_save(BankAccount.FILENAME, accounts_info)

    @classmethod
    def create_account(
        cls,
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
            cls.json_save(BankAccount.FILENAME, {})
            logger.debug("Created bank accounts JSON database.")
        else:
            BankAccount.accounts_info = cls.json_import(BankAccount.FILENAME)
            logger.debug("Read accounts info from JSON database.")

        new_account = cls(national_id, account_name, first_name, last_name, balance, password)

        if national_id in BankAccount.accounts_info:
            new_account.accounts = BankAccount.accounts_info[new_account.national_id]
            new_account.accounts.update({new_account.account_name: new_account.__dict__})
            BankAccount.accounts_info.update({new_account.national_id: new_account.accounts})
        else:
            data.update({new_account.national_id: {new_account.account_name: new_account.__dict__}})
            logger.debug("Added new bank account to JSON database.")
        cls.json_save(BankAccount.FILENAME, data)

    def __str__(self) -> str:
        """Cutomize print output of object."""
        return f"""
        National ID: {self.national_id}
        Name: {self.first_name},
        Last: {self.last_name},
        Balance: {self._balance},
        Password: {self._password},
        creation_date: {self.creation_date},
        cvv2: {self.cvv2}
        """
    
def main():
    if platform.system() == "Linux":
        clear_cmd = "clear"
    else:
        clear_cmd = "cls"

    while True:
        user_command = input(
            """
            1. Create new bank account.
            2. Deposit
            3. Withdraw
            4. Exit
            Insert your command: """)
        os.system(clear_cmd)
        match user_command:
            case "1":
                id = input("National ID: ")
                account_name = input("Yor account name: ")
                first_name = input("First name: ")
                last_name = input("Last name: ")
                balance = int(input("Initial balance: "))
                password = input("Transaction password: ")
                BankAccount.create_account(id, account_name, first_name, last_name, balance, password)

                accounts_info = BankAccount.json_import(BankAccount.FILENAME)
                created_account = accounts_info[id]
                print(
                    f"""
                    Successfully created bank account for {created_account[account_name]["national_id"]}
                    National ID: {created_account[account_name]["national_id"]},
                    Accounts: {list(created_account.keys())}
                    First Name: {created_account[account_name]["first_name"]},
                    Last Name: {created_account[account_name]["last_name"]},
                    Balance: {created_account[account_name]["_balance"]},
                    Password: {created_account[account_name]["_password"]},
                    CVV2: {created_account[account_name]["cvv2"]}
                    """)
                input("Press enter to go next .... ")
                os.system(clear_cmd)
            case "2":
                id = input("National ID: ")
                account_name = input("Yor account name: ")
                password = input("Transaction password: ")
                cvv2 = int(input("CVV2: "))
                deposit_amount = int(input("How much for deposit? "))
                BankAccount.deposit(id, account_name, password, cvv2, deposit_amount)
                accounts_info = BankAccount.json_import(BankAccount.FILENAME)
                created_account = accounts_info[id]
                print(
                    f"""Succecfully dposited {deposit_amount}. Now, your balance is {created_account[account_name]["_balance"]}
                    """)
                input("Press enter to go next ....")
                os.system(clear_cmd)
            case "3":
                id = input("National ID: ")
                account_name = input("Yor account name: ")
                password = input("Transaction password: ")
                cvv2 = int(input("CVV2: "))
                withdraw_amount = int(input("How much for deposit? "))
                BankAccount.withdraw(id, account_name, password, cvv2, withdraw_amount)
                accounts_info = BankAccount.json_import(BankAccount.FILENAME)
                created_account = accounts_info[id]
                print(
                    f"""Succecfully withdrawed {withdraw_amount}. Now, your balance is {created_account[account_name]["_balance"]}
                    """)
                input("Press enter to go next ....")
                os.system(clear_cmd)
            case "4":
                break


if __name__ == "__main__":
    main()
