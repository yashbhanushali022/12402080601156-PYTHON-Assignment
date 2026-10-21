# Q5 - Object-Oriented Bank Settlement System

class BankError(Exception):
    pass


class AccountNotFoundError(BankError):
    pass


class InsufficientBalanceError(BankError):
    pass


class Account:

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount):

        if amount <= 0:
            raise BankError("Invalid amount")

        self.balance += amount

    def withdraw(self, amount):

        if amount <= 0:
            raise BankError("Invalid amount")

        if amount > self.balance:
            raise InsufficientBalanceError(
                "Insufficient balance"
            )

        self.balance -= amount


class Transaction:

    def __init__(self, operation, account, amount=0,
                 destination=None):

        self.operation = operation
        self.account = account
        self.amount = amount
        self.destination = destination


class Bank:

    def __init__(self):
        self.accounts = {}

    def add_account(self, account_id, balance):
        self.accounts[account_id] = Account(
            account_id,
            balance
        )

    def get_account(self, account_id):

        if account_id not in self.accounts:
            raise AccountNotFoundError(
                "Account does not exist"
            )

        return self.accounts[account_id]

    def deposit(self, account_id, amount):

        self.get_account(account_id).deposit(amount)

    def withdraw(self, account_id, amount):

        self.get_account(account_id).withdraw(amount)

    def transfer(self, source, destination, amount):

        source_account = self.get_account(source)
        destination_account = self.get_account(destination)

        source_account.withdraw(amount)
        destination_account.deposit(amount)


# Read accounts
bank = Bank()

number_of_accounts = int(input())

for _ in range(number_of_accounts):

    account_id, balance = input().split()

    bank.add_account(
        account_id,
        int(balance)
    )


q = int(input())

batch_number = 0
batch_active = False
batch_backup = {}
failed_batches = []

for _ in range(q):

    line = input().split()

    operation = line[0]

    try:

        if operation == "BATCH_BEGIN":

            batch_number += 1
            batch_active = True

            batch_backup = {
                account_id: account.balance
                for account_id, account
                in bank.accounts.items()
            }

        elif operation == "BATCH_END":

            batch_active = False
            batch_backup = {}

        elif operation == "DEPOSIT":

            account = line[1]
            amount = int(line[2])

            bank.deposit(account, amount)

        elif operation == "WITHDRAW":

            account = line[1]
            amount = int(line[2])

            bank.withdraw(account, amount)

        elif operation == "TRANSFER":

            source = line[1]
            destination = line[2]
            amount = int(line[3])

            bank.transfer(
                source,
                destination,
                amount
            )

    except BankError:

        if batch_active:

            for account_id, balance in batch_backup.items():
                bank.accounts[account_id].balance = balance

            failed_batches.append(batch_number)

            batch_active = False
            batch_backup = {}


if failed_batches:
    for number in failed_batches:
        print("FAILED", number)


for account_id in sorted(bank.accounts):

    print(
        account_id,
        bank.accounts[account_id].balance
    )