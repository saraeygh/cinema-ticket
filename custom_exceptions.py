"""
This module is for my custom Exceptions
"""


class ShortPasswordError(Exception):
    """
    I use this Error when Short Password has been Entered.
    """


class PasswordError(Exception):
    """
    I use this Error when Wrong Password has been Entered.
    """


class UserError(Exception):
    """
    I use this Error When Wrong Username has been Entered.
    """


class RepUserError(Exception):
    """
    I use this Error When Repetitious Username has been Entered.
    """


class TwoPasswordError(Exception):
    """
    I use this Error When two New Passwords are not Match.
    """


class InvalidNationalID(Exception):
    """
    Used for invalid national ID.
    """


class BalanceMinimum(Exception):
    """
    Used for minimum balance error.
    """


class FileError(Exception):
    """
    I use this Error When File Not Found.
    """


class UnsuccessfulDeposit(Exception):
    """
    When deposit was unsuccessful.
    """


class UnsuccessfulWithdraw(Exception):
    """
    When Withdraw was unsuccessful.
    """


class FilmError(Exception):
    """
    I use this Error when Film Not found.
    """


class NoCapacityError(Exception):
    """
    I use this Error when No sufficient tickets available.
    """
