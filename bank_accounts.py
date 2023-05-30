import os
import random
from human import Human
from datetime import datetime
import custom_exceptions
import logging

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
    accounts_dict = {}

    def __init__(
        self,
        national_id: str,
        first_name: str,
        last_name: str,
        balance: float,
        password: str,
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
        self.first_name = first_name
        self.last_name = last_name
        self._balance = balance
        self._password = Human.hashing(password)
        self.creation_date = str(datetime.now())
        self.cvv2 = random.randint(1111, 9999)
        
    @staticmethod
    def national_id_valid(national_id: str) -> bool:
        """Chechs whether national ID is ten digits.

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
        if balance < 10_000:
            logger.debug(f"Balance can not be less that Minimum {BankAccount.MIN_BALANCE}.")
            raise custom_exceptions.BalanceMinimum("Invalid balance.")
        logger.debug(f"Set balance = {self._balance} for national ID {self.national_id}")
        self._balance = balance

    @property
    def password(self) -> str:
        """Password Getter

        Returns:
            str: Password as string.
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Password Setter

        Args:
            password (str): Inputed password.
        """
        if not Human.password_check(password):
            logger.debug(f"Password was short and not changed for national ID {self.national_id}")
            raise custom_exceptions.ShortPasswordError("Too short Password!")
        logger.debug(f"Password changed for national ID {self.national_id}")
        password = Human.hashing(password)
        self._password = password

    def deposit(self, national_id, password, cvv2, amount: int):
        """Deposit method

        Args:
            amount (int): Amount to deposit.

        Raises:
            custom_exceptions.BalanceMinimum: If balance goes down the min limit.
        """
        accounts_info = Human.json_import(BankAccount.FILENAME)
        if not national_id in accounts_info:
            logger.debug(f"Unsuccessful deposit, {self.national_id} not found.")
            raise custom_exceptions.UnsuccessfulDeposit("Unsuccessful deposit, national ID not found.")
        if Human.hashing(password) != accounts_info[national_id]["_password"]:
            logger.debug(f"Unsuccessful deposit, Wrong password.")
            raise custom_exceptions.UnsuccessfulDeposit("Unsuccessful deposit, Wrong password.")
        if cvv2 != accounts_info[national_id]["cvv2"]:
            logger.debug(f"Unsuccessful deposit, {self.cvv2} for CVV2 is wrong.")
            raise custom_exceptions.UnsuccessfulDeposit("Unsuccessful deposit, Wrong CVV2.")
        if self._balance + amount < self.MIN_BALANCE:
            logger.debug(f"Unsuccessful deposit, Balance cant be less than {BankAccount.MIN_BALANCE}.")
            raise custom_exceptions.BalanceMinimum("Invalid balance.")
        
        logger.debug(f"Successfully deposited {amount} to {self.national_id} bank account.")
        self._balance += amount
        accounts_info[national_id]["_balance"] = self._balance
        Human.json_save(BankAccount.FILENAME, accounts_info)

    def withdraw(self, national_id, password, cvv2, amount: int):
        """Withdraw method

        Args:
            amount (int): Amount to withdraw.

        Raises:
            custom_exceptions.BalanceMinimum: If balance goes down the min limit.
        """
        accounts_info = Human.json_import(BankAccount.FILENAME)
        if not national_id in accounts_info:
            logger.debug(f"Unsuccessful withdraw, {self.national_id} not found.")
            raise custom_exceptions.UnsuccessfulWithdraw("Unsuccessful withdraw, national ID not found.")
        if Human.hashing(password) != accounts_info[national_id]["_password"]:
            logger.debug(f"Unsuccessful withdraw, Wrong password.")
            raise custom_exceptions.UnsuccessfulWithdraw("Unsuccessful withdraw, Wrong password.")
        if cvv2 != accounts_info[national_id]["cvv2"]:
            logger.debug(f"Unsuccessful Withdraw, {self.cvv2} for CVV2 is wrong.")
            raise custom_exceptions.UnsuccessfulWithdraw("Unsuccessful Withdraw, Wrong CVV2.")
        if self._balance + amount < self.MIN_BALANCE:
            logger.debug(f"Unsuccessful Withdraw, Balance cant be less than {BankAccount.MIN_BALANCE}.")
            raise custom_exceptions.BalanceMinimum("Invalid balance.")
        
        logger.debug(f"Successfully Withdrawed {amount} from {self.national_id} bank account.")
        self._balance -= amount
        accounts_info[national_id]["_balance"] = self._balance
        Human.json_save(BankAccount.FILENAME, accounts_info)

    @staticmethod
    def create_account(
        national_id: int,
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
        new_account = BankAccount(national_id, first_name, last_name, balance, password)
        if not os.path.exists(BankAccount.FILENAME):
            Human.json_create(BankAccount.FILENAME)
            logger.debug("Created bank accounts JSON database.")
        data = Human.json_import(BankAccount.FILENAME)
        logger.debug("Read accounts info from JSON database.")
        data.update({new_account.national_id: new_account.__dict__})
        logger.debug("Added new bank account to JSON database.")
        Human.json_save(BankAccount.FILENAME, data)

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
    pass
    
if __name__ == "__main__":
    main()