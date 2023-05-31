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

class UnsuccessfulIdDeposit(Exception):
    """
    Use This Error for wrong ID
    """


class UnsuccessfulAccountDeposit(Exception):
    """
    Use this Error for wrong Account Name
    """


class UnsuccessfulPasswordDeposit(Exception):
    """
    Use this Error for Wrong account Password
    """


class UnsuccessfulCvv2Deposit(Exception):
    """
    Use this Error for Wrong CVV2
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


class PhoneNumberError(Exception):
    """
    I use this Error when invalid phone number format has entered.
    """

class AlreadyExistAccount(Exception):
    """
    when account name already exists.
    """


class AddTicketFailed(Exception):
    """raised when add ticket for film failed."""


class TicketError(Exception):
    """
    Ticket Error
    """
