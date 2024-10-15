#IMPORTING MODULES
import mysql.connector as ms
import random
from datetime import datetime, timedelta
from decimal import Decimal
from prettytable import PrettyTable

#SETTING UP MYSQL MOUDULE
mydb= ms.connect(host = 'localhost' , user = 'root' , password = 'A@bcd123')
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE if not exists Bank")
mycursor.execute("USE Bank")

#FUNCTIONS
def account_displayer():
    mycursor.execute("SELECT * FROM accounts")
    rows = mycursor.fetchall()
    if not rows:
        print("No records found.")
    else:
        table = PrettyTable()
        table.field_names = ["Account Number", "PIN", "Account Holder's Name", "Age", "Balance", 
                             "Date Registered", "Account Type", "Branch Name", "Last Transaction Date"]
        for row in rows:
            table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
        print("Account Details:")
        print(table)

def search_account_details(Account_Number):
    if Account_Number == 0:
        return
    mycursor.execute("SELECT * FROM accounts WHERE account_number = %s", (Account_Number,))
    account_details = mycursor.fetchone()

    if account_details is None:
        print("Account not found.")
    else:
        print("\nAccount Details:")
        print("Account Number:", account_details[0])
        print("PIN:", account_details[1])
        print("Account Holder's Name:", account_details[2])
        print("Age:", account_details[3])
        print("Balance:", account_details[4])
        print("Date Registered:", account_details[5])
        print("Account Type:", account_details[6])
        print("Branch Name:", account_details[7])
        print("Last Transaction Date:", account_details[8], "\n")

branches = ["Dubai Mall", "Madinate Badr", "Al Maktoum Branch", "Business Bay", "Abu Al Souq", "Shaikh Zayed Road", "Onyx Tower", "Bur Dubai", "Jumeriah", "DIC", "Al Twar", "Umm Suqeim", "Ibn Battuta Mall", "Oud Meitha", "Al Lisaili", "Muhaisnah Al Ittihad Mall", "Wajaha Maktoom Road", "Mall of the Emirates", "Al Ittihad Mall", "Emirates Headquarters", "Hatta", "Reef Mall", "City Centre Mirdif", "Emirates Cooperative Society Al Twar 3", "Al Nahda", "Abu Dhabi", "Al Salam", "Al Wahda Mall", "Al Muroor", "Bawabat Al Sharq Mall", "Deerfields Mall", "Dalma Mall", "Al Dhafra Mall", "Al Ain", "Al Ain Mall", "Al Jimi", "Al Aliah Mall", "Sharjah", "Wasit Road", "Sharjah Clock Tower", "Al Dhaid", "Al Madam", "Sahara Centre", "Al Qarrayn", "Tasjeel", "Al Zahia City Center", "Kalba", "Ajman", "Al Humaideya", "Ras Al Khaimah", "Khuzam", "Julphar", "Mall of UAQ", "Khor Fakkan", "Fujairah", "Dibba-Fujairah"]
account_types = ["Savings Account", "Checking Account", "Escrow Account", "Fixed Deposit", "Al Islami Current Account", "Current Account"]

def new_account_holder():
    while True:
        try:
            account_holder_name = input("Enter account holder's Name: ")
            if account_holder_name == '00':
                break
            elif not account_holder_name.isalpha():
                print("Name must be a string value")
                break

            age = int(input("Enter account holder's Age: "))
            if age == 00 or not 18 <= age <= 100:
                print("Age must be between 18 and 100")
                continue

            balance = float(input("Enter account Balance: "))
            if balance == 00 or balance > 999999999 or balance < 0:
                print("Invalid balance value.")
                continue

            account_type = input("Enter the account type: ")
            if account_type == '00' or account_type not in account_types:
                print("Invalid account type. Please enter a valid type.")
                continue

            branch_name = input("Enter the branch name: ")
            if branch_name == '00' or branch_name not in branches:
                print("Invalid branch name. Please enter a valid branch.")
                continue

            pin = random.randint(1000000, 9999999)
            mycursor.execute("""
                INSERT INTO accounts
                (PIN, Account_Holder_Name, Age, Balance, Date_Registered, Account_Type, Branch_Name, Last_Transaction_Date)
                VALUES (%s, %s, %s, %s, CURRENT_DATE, %s, %s, NOW())
            """, (pin, account_holder_name, age, balance, account_type, branch_name))
            mydb.commit()

            print("Account Created Successfully.")
            print("Your 7-digit PIN:", pin)
            break

        except ValueError:
            print("Invalid input format. Please enter numeric values for age and balance.")
            return

def account_deleter(Account_Number):
    if Account_Number == 00:
        return
    mycursor.execute("SELECT * FROM Loan WHERE Account_Number = {}".format(Account_Number))
    existing_loan = mycursor.fetchone()
    if existing_loan:
        print("Cannot delete the account. It has a loan pending.")
        return
    mycursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(Account_Number))
    existing_account = mycursor.fetchone()
    if existing_account is None:
        print("Account not found.")
        return
    print("Existing details:")
    search_account_details(Account_Number)
    confirmation = input(f"Do you want to delete the account with number {Account_Number}? (yes/no): ").lower()
    if confirmation == "yes":
        mycursor.execute("""
            INSERT INTO deleted_accounts
            (account_number, pin, account_holder_name, age, balance, date_registered, account_type, branch_name, last_transaction_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, existing_account)
        mycursor.execute("DELETE FROM accounts WHERE account_number = {}".format(Account_Number))
        mydb.commit()

        print("Account deleted successfully.")
        print("Updated details:")
        search_account_details(Account_Number)
    else:
        print("Account deletion canceled.")

def new_transaction(account_number, receiving_account_number, transaction_amount):
    mycursor.execute("SELECT balance FROM accounts WHERE account_number = {}".format(account_number))
    balance = mycursor.fetchone()
    if transaction_amount > balance[0]:
        print("You don't have enough balance to make this transaction")
        return

    pin = int(input("Enter your PIN for account {}: ".format(account_number)))

    mycursor.execute("SELECT pin FROM accounts WHERE account_number = {}".format(account_number))
    correct_pin = mycursor.fetchone()[0]

    if pin != correct_pin:
        print("Incorrect PIN. Transaction aborted.")
        return

    transaction_time = "NOW()"

    mycursor.execute("""
        UPDATE accounts
        SET balance = balance - {},
            last_transaction_date = {}
        WHERE account_number = {}
    """.format(transaction_amount, transaction_time, account_number))
    mycursor.execute("""
        UPDATE accounts
        SET balance = balance + {},
            last_transaction_date = {}
        WHERE account_number = {}
    """.format(transaction_amount, transaction_time, receiving_account_number))
    mycursor.execute("""
        INSERT INTO transactions
        (Account_Number, Reciving_Account_Number, Transaction_Time, Transaction_Amount)
        VALUES ({}, {}, {}, {})
    """.format(account_number, receiving_account_number, transaction_time, transaction_amount))
    mydb.commit()
    print("Transaction and account balances updated successfully.")
    
def personal_transaction_details(account_number):
    mycursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(account_number))
    existing_account = mycursor.fetchone()
    if existing_account is None:
        print("Account not found.")
        return
    mycursor.execute("""
        SELECT * FROM transactions
        WHERE Account_Number = {} OR Reciving_Account_Number = {}
        ORDER BY Transaction_Time
    """.format(account_number, account_number))
    transactions = mycursor.fetchall()
    if not transactions:
        print("No transactions found for account {}.".format(account_number))
    else:
        table = PrettyTable()
        table.field_names = ["Transaction Time", "Transaction Type", "Amount", "Counterparty Account", "Transaction Number"]
        for transaction in transactions:
            transaction_time = transaction[2]
            amount = transaction[3]
            counterparty_account = transaction[1] if transaction[0] == account_number else transaction[0]
            transaction_type = "Giving" if transaction[0] == account_number else "Receiving"
            transaction_number = transaction[4]
            table.add_row([transaction_time, transaction_type, amount, counterparty_account, transaction_number])
        print("Transaction Details for Account {}:".format(account_number))
        print(table)

def loan_repayment_statement():
    account_number = int(input("Enter the account number: "))
    mycursor.execute("SELECT * FROM Loan WHERE Account_Number = %s", (account_number,))
    existing_loan = mycursor.fetchone()

    if existing_loan is None:
        print("No loan found for the account.")
        return

    print("Loan Details:")
    print("Loan Number:", existing_loan[0])
    print("Account Number:", existing_loan[1])
    print("Principal Amount:", existing_loan[2])
    print("Profit Rate:", existing_loan[3])
    print("Time Period (Months):", existing_loan[4])
    print("Loan Type:", existing_loan[5])
    print("Customer Salary:", existing_loan[6])
    print("Final Amount:", existing_loan[7])
    print("Total Profit:", existing_loan[8])
    print("Remaining Amount:", existing_loan[9])
    print("Last Payment Date:", existing_loan[10])

    total_repayment = float(input("Enter the total repayment amount: "))

    if total_repayment == 0:
        print("Repayment amount cannot be zero. Exiting function.")
        return
    elif total_repayment < 0:
        print("Invalid repayment amount. Amount must be greater than 0.")
        return
    elif Decimal(total_repayment) > existing_loan[9]:
        print("Invalid repayment amount. Amount cannot exceed the remaining balance.")
        return

    remaining_balance = existing_loan[9] - Decimal(total_repayment)
    mycursor.execute("""
        UPDATE Loan
        SET Remaining_Amount = %s, Last_Payment = NOW()
        WHERE Account_Number = %s
    """, (remaining_balance, account_number))
    mydb.commit()

    if remaining_balance == 0:
        mycursor.execute("""
            INSERT INTO Paid_Loans
            (Account_Number, Principal_Amount, Profit_Rate, Time_Period_in_months, Loan_Type, Customer_Salary, 
            Final_Amount, Total_Profit, Remaining_Amount, Last_Payment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, existing_loan[1:])
        mydb.commit()

        mycursor.execute("DELETE FROM Loan WHERE Account_Number = %s", (account_number,))
        mydb.commit()

        print("Loan fully repaid. Entry moved to Paid_Loans table.")
    else:
        print("\nRepayment Statement:")
        print("Repayment Date:", datetime.now())
        print("Total Repayment Amount:", total_repayment)
        print("Remaining Balance:", remaining_balance)
