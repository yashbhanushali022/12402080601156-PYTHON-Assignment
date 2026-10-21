# Q4 - Exception-Safe CSV Transaction Splitter

import csv
from datetime import datetime

filename = input().strip()

balances = {}

with open(filename, "r", newline="") as file:

    reader = csv.DictReader(file)

    with open("credit.csv", "w", newline="") as credit_file, \
         open("debit.csv", "w", newline="") as debit_file, \
         open("error.csv", "w", newline="") as error_file:

        credit_writer = csv.writer(credit_file)
        debit_writer = csv.writer(debit_file)
        error_writer = csv.writer(error_file)

        header = ["transaction_id", "account_id",
                  "type", "amount", "timestamp"]

        credit_writer.writerow(header)
        debit_writer.writerow(header)

        error_writer.writerow(
            ["transaction_id", "account_id",
             "type", "amount", "timestamp", "reason"]
        )

        for row in reader:

            try:
                transaction_id = row["tid"]
                account_id = row["acc"]
                transaction_type = row["type"]
                amount_text = row["amount"]
                timestamp = row["time"]

                amount = float(amount_text)

                if amount <= 0:
                    raise ValueError("Amount must be positive")

                if transaction_type not in ["CREDIT", "DEBIT"]:
                    raise ValueError("Invalid transaction type")

                datetime.strptime(
                    timestamp,
                    "%Y-%m-%dT%H:%M:%S"
                )

                if account_id not in balances:
                    balances[account_id] = 0

                if transaction_type == "CREDIT":

                    balances[account_id] += amount

                    credit_writer.writerow([
                        transaction_id,
                        account_id,
                        transaction_type,
                        amount,
                        timestamp
                    ])

                else:

                    balances[account_id] -= amount

                    debit_writer.writerow([
                        transaction_id,
                        account_id,
                        transaction_type,
                        amount,
                        timestamp
                    ])

            except Exception as error:

                error_writer.writerow([
                    row.get("tid", ""),
                    row.get("acc", ""),
                    row.get("type", ""),
                    row.get("amount", ""),
                    row.get("time", ""),
                    str(error)
                ])


# Sort by absolute balance change
sorted_balances = sorted(
    balances.items(),
    key=lambda x: abs(x[1]),
    reverse=True
)

for account, balance in sorted_balances:
    if balance.is_integer():
        print(account, int(balance))
    else:
        print(account, balance)

print("Files created: credit.csv, debit.csv, error.csv")