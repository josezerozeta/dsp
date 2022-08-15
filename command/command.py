import unittest
from abc import ABC
from enum import Enum


class BankAccount:
    OVERDRAFT_LIMIT = -500

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f'Deposited {amount}, '
              f'balance = {self.balance}')

    def withdraw(self, amount):
        if self.balance - amount >= BankAccount.OVERDRAFT_LIMIT:
            self.balance -= amount
            print(f'Withdrew {amount}, '
                  f'balance = {self.balance}')
            return True
        return False

    def __str__(self):
        return f'Balance = {self.balance}'


class Command(ABC):

    def __init__(self):
        self.success = False

    def invoke(self):
        pass

    def undo(self):
        pass


class BankAccountCommand(Command):
    class Action(Enum):
        DEPOSIT = 0
        WITHDRAW = 1

    def __init__(self, account, action, amount):
        super(BankAccountCommand, self).__init__()
        self.amount = amount
        self.action = action
        self.account = account

    def invoke(self):
        if self.action == self.Action.DEPOSIT:
            self.account.deposit(self.amount)
            self.success = True
        elif self.action == self.Action.WITHDRAW:
            self.success = self.account.withdraw(self.amount)

    def undo(self):
        if not self.success:
            return

        if self.action == self.Action.DEPOSIT:
            self.account.withdraw(self.amount)
        elif self.action == self.Action.WITHDRAW:
            self.account.deposit(self.amount)


class CompositeBankAccountCommand(Command, list):
    def __init__(self, items=[]):
        super(CompositeBankAccountCommand, self).__init__()
        for item in items:
            self.append(item)

    def invoke(self):
        for command in self:
            command.invoke()

    def undo(self):
        for command in reversed(self):
            command.undo()


class MoneyTransferCommand(CompositeBankAccountCommand):
    def __init__(self, from_acct, to_acct, amount):
        super(MoneyTransferCommand, self).__init__([
            BankAccountCommand(from_acct, BankAccountCommand.Action.WITHDRAW, amount),
            BankAccountCommand(to_acct, BankAccountCommand.Action.DEPOSIT, amount)
        ])

    def invoke(self):
        ok = True
        for command in self:
            if ok:
                command.invoke()
                ok = command.success
            else:
                command.success = False
        self.success = ok


class TestSuite(unittest.TestCase):
    def test_composite_deposit(self):
        ba = BankAccount()
        deposit1 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 100)
        deposit2 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 50)
        composite = CompositeBankAccountCommand([deposit1, deposit2])
        composite.invoke()
        print(ba)
        composite.undo()
        print(ba)

    def test_transfer(self):
        ba1 = BankAccount(100)
        ba2 = BankAccount()

        amount = 100

        transfer = MoneyTransferCommand(ba1, ba2, amount)
        transfer.invoke()
        print(f'ba1: {ba1}, ba2: {ba2}')
        transfer.undo()
        print(f'ba1: {ba1}, ba2: {ba2}')
        print(transfer.success)