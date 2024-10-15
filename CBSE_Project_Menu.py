#IMPORTING MODULES
import mysql.connector as ms
import random
from datetime import datetime, timedelta
from decimal import Decimal
from prettytable import PrettyTable
from CBSE_Project_Employee import *
from CBSE_Project_Manager import *

def welcome():
    print('''
                                        --------------------------------------------------------------
                                        |                            WELCOME                          |
                                        |                              TO                             |
                                        |                      DUBAI ISLAMIC BANK                     |
                                        --------------------------------------------------------------
    ''')

def main_menu():
    print('''
                                        --------------------------------------------------------------
                                        |                  Type 1 FOR USING ADMIN PORTAL              |
                                        |                Type 2 FOR USING EMPLOYEE PORTAL             |
                                        |                      Click 0 FOR EXIT                       |
                                        --------------------------------------------------------------
    ''')

#0
def display_menu_Manager():
    print('''
    1. Manage Accounts
    2. Manage Transactions
    3. Manage Loans
    4. Manage Employees
    0. Exit
    ''')

#1
def display_menu_manage_Accounts():
    print('''
    1. Display Account Details
    2. Search Account Details
    3. New Account Holder
    4. Delete Account
    5. Modify Account Details
    6. View Deactivated Accounts
    0. Exit
    ''')

#2
def display_menu_manage_Transactions():
    print('''
    1. Display Transactions
    2. New Transaction 
    3. View Personal Transaction Details
    0. Exit
    ''')

#3
def display_menu_manage_Loans():
    print('''
    1. Display Loans
    2. New Loans 
    3. Loan Lay Off
    4. Modify Loan Details
    5. View Specific Loan Details
    6. View Paid Loans
    0. Exit
    ''')

#4
def display_menu_manage_Employees():
    print('''
    1. Display Employee Details 
    2. New Employee
    3. Delete Employee 
    4. Modify Employee Details
    5. View Specific Employee Details
    0. Exit
    ''')       

def main_Manager():
    while True:
        try:
            display_menu_Manager()
            mainchoice = input("\nEnter your choice (0-4): ")
            if mainchoice == "0":
                print("Exiting the program. Goodbye!")
                break
            elif mainchoice == "1":
                while True:
                    try:
                        display_menu_manage_Accounts()
                        subchoice = input("\nEnter your choice (0-6): ")
                        if subchoice == "0":
                            break
                        elif subchoice == "1":
                            account_displayer()
                        elif subchoice == "2":
                            Account_Number = int(input("Enter Account Number to view details: "))
                            search_account_details(Account_Number)
                        elif subchoice == "3":
                            new_account_holder()
                        elif subchoice == "4":
                            Account_Number = int(input("Enter Account Number to Delete: "))
                            account_deleter(Account_Number)
                        elif subchoice == "5":
                            Account_Number = int(input("Enter Account Number to Modify: "))
                            account_modificator(Account_Number)
                        elif subchoice == "6":
                            display_deleted_accounts()
                        else:
                            print("INVALID Choice. Please Enter a valid choice.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

            elif mainchoice == "2":
                while True:
                    try:
                        display_menu_manage_Transactions()
                        subchoice = input("\nEnter your choice (0-3): ")
                        if subchoice == "0":
                            break
                        elif subchoice == "1":
                            transaction_displayer()
                        elif subchoice == "2":
                            while True:
                                try:
                                    account_number = int(input("Enter account number for the account giving money: "))
                                    if account_number == 0:
                                        break
                                    mycursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(account_number))
                                    existing_account = mycursor.fetchone()
                                    if existing_account is None:
                                        print("Account not found in the accounts table. Please enter a valid account number.")
                                    else:
                                        reciving_account_number = int(input("Enter account number for the account receiving money: "))
                                        if reciving_account_number == 0:
                                            break
                                        mycursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(reciving_account_number))
                                        existing_account = mycursor.fetchone()
                                        if existing_account is None or reciving_account_number == account_number:
                                            print("Account not found in the accounts table. Please enter a valid account number.")
                                        else:
                                            transaction_amount = float(input("Enter the transaction amount: "))
                                            if transaction_amount == 0:
                                                break
                                            new_transaction(account_number, reciving_account_number, transaction_amount)
                                            break
                                except ValueError:
                                    print("Invalid input. Please enter a valid number.")

                        elif subchoice == "3":
                            account_number_to_check = int(input("Enter Account Number to View Transaction Details: "))
                            if account_number_to_check == 0:
                                break
                            personal_transaction_details(account_number_to_check)
                        else:
                            print("INVALID Choice. Please Enter a Number a valid choice.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

            elif mainchoice == "3":
                while True:
                    try:
                        display_menu_manage_Loans()
                        subchoice = input("\nEnter your choice (0-6): ")
                        if subchoice == "0":
                            break
                        if subchoice == '1':
                            loans_displayer()
                        elif subchoice == "2":
                            account_number = int(input("Enter account number for the account taking the loan: "))
                            if account_number == 0:
                                break
                            mycursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(account_number))
                            existing_account = mycursor.fetchone()
                            if existing_account is None:
                                print("Account not found in the accounts table. Please enter a valid account number.")
                            else:
                                grant_loan(account_number)
                        elif subchoice == "3":
                            account_number = int(input("Enter account number whose loan is being written off: "))
                            loan_deleter(account_number)
                        elif subchoice == "4":
                            Account_Number = int(input("Enter account number to modify loan details: "))
                            loan_modifier(Account_Number)
                        elif subchoice == "5":
                            account_number = int(input("Enter account number to view loan details: "))
                            loan_details_displayer(account_number)
                        elif subchoice == "6":
                            display_paid_loans()
                        else:
                            print("INVALID Choice. Please Enter a Number a valid choice.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

            elif mainchoice == "4":
                while True:
                    try:
                        display_menu_manage_Employees()
                        subchoice = input("\nEnter your choice (0-5): ")
                        if subchoice == "0":
                            break
                        elif subchoice == "1":
                            employee_displayer()
                        elif subchoice == "2":
                            new_employee()
                        elif subchoice == "3":
                            employee_id = int(input("Enter the Employee_ID to delete: "))
                            employee_deleter(employee_id)
                        elif subchoice == "4":
                            employee_id = int(input("Enter the Employee_ID to modify: "))
                            employee_details_modifier(employee_id)
                        elif subchoice == "5":
                            employee_id = int(input("Enter the Employee_ID to view details: "))
                            employee_details_displayer(employee_id)
                        else:
                            print("INVALID Choice. Please Enter a Number a valid choice.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
            else:
                print("INVALID Choice. Please Enter a Number a valid choice.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def display_menu_Employee():
    print("\nMENU:")
    print("1. Display Account Details")
    print("2. Search Account Details")
    print("3. New Account Holder")
    print("4. Delete Account")
    print("5. New Transaction")
    print("6. Personal Transaction Details")
    print("7. Loan Repayment")
    print("0. Exit")

def main_Employee():
    while True:
        try:
            display_menu_Employee()
            choice = input("\nEnter your choice (0-7): ")

            if choice == "0":
                print("Exiting the program. Goodbye!")
                return
            elif choice == "1":
                account_displayer()
            elif choice == "2":
                Account_Number = int(input("Enter Account Number to view details: "))
                search_account_details(Account_Number)
            elif choice == "3":
                new_account_holder()
            elif choice == "4":
                Account_Number = int(input("Enter Account Number to Delete: "))
                account_deleter(Account_Number)
            elif choice == "5":
                while True:
                    try:
                        account_number = int(input("Enter account number for the account giving money: "))
                        if account_number == 00:
                            break
                        mycursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(account_number))
                        existing_account = mycursor.fetchone()    
                        if existing_account is None:
                            print("Account not found in the accounts table. Please enter a valid account number.")
                        else:
                            reciving_account_number = int(input("Enter account number for the account receiving money: "))
                            if reciving_account_number == 00:
                                break
                            mycursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(reciving_account_number))
                            existing_account = mycursor.fetchone()    
                            if existing_account is None or reciving_account_number == account_number:
                                print("Account not found in the accounts table. Please enter a valid account number.")
                            else:
                                transaction_amount = float(input("Enter the transaction amount: "))
                                if transaction_amount == 00:
                                    break
                                else:
                                    new_transaction(account_number, reciving_account_number, transaction_amount)
                                    break
                    except Exception as e:
                        print(f"Error: {e}")
            elif choice == "6":
                account_number = int(input("Enter Account Number to View Transaction Details: "))
                if account_number == 00:
                    break
                else:
                    personal_transaction_details(account_number)
            elif choice == "7":
                loan_repayment_statement()
            else:
                print("Invalid choice. Please enter a number between 0 and 7.")
        except Exception as e:
            print(f"Error: {e}")
