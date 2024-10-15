# IMPORTING MODULES
import mysql.connector as ms
import random
from datetime import datetime, timedelta
from decimal import Decimal
from prettytable import PrettyTable
from CBSE_Project_Employee import *
from CBSE_Project_Manager import *
from CBSE_Project_Menu import *

# SETTING UP MYSQL MODULE
mydb = ms.connect(host='localhost', user='root', password='A@bcd123')
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS Bank")
mycursor.execute("USE Bank")

# CREATING TABLE employee_details
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS employee_details (
        Employee_ID INT AUTO_INCREMENT PRIMARY KEY,
        First_Name VARCHAR(50),
        Last_Name VARCHAR(50),
        Date_of_Birth DATE,
        Gender VARCHAR(10),
        Phone_Number CHAR(13),
        Password INT(8),
        Department VARCHAR(50),
        Job_Title VARCHAR(50),
        Clearance_Level CHAR(1),
        Date_of_Joining DATE
    ) AUTO_INCREMENT = 1000
''')

# CREATING TABLE employee_salaries AND LINKING IT TO employee_details TABLE USING FOREIGN KEY
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS employee_salaries (
        Salary_ID INT AUTO_INCREMENT PRIMARY KEY,
        Employee_ID INT,
        Salary DECIMAL(10, 2),
        Payment_Date DATE,
        CONSTRAINT fk_employee_salaries_employee_id FOREIGN KEY (Employee_ID) REFERENCES employee_details(Employee_ID)
    )
''')

# CREATING TABLE accounts
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_number INT AUTO_INCREMENT PRIMARY KEY,
        pin INT(8),
        account_holder_name VARCHAR(255),
        age INT,
        balance DECIMAL(10, 2),
        date_registered DATE,
        account_type VARCHAR(50),
        branch_name VARCHAR(100),
        last_transaction_date TIMESTAMP
     ) AUTO_INCREMENT = 1000000000
''')

# CREATING TABLE deleted_accounts
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS deleted_accounts (
        account_number INT AUTO_INCREMENT PRIMARY KEY,
        pin INT(8),
        account_holder_name VARCHAR(255),
        age INT,
        balance DECIMAL(10, 2),
        date_registered DATE,
        account_type VARCHAR(50),
        branch_name VARCHAR(100),
        last_transaction_date TIMESTAMP
    ) AUTO_INCREMENT = 1000000000
''')

# CREATING TABLE Transactions
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Transactions (
        Account_Number INT,
        Reciving_Account_Number INT,
        Transaction_Time TIMESTAMP,
        Transaction_Amount Decimal(10,2),
        Transaction_Number INT AUTO_INCREMENT PRIMARY KEY   
    )
''')

# CREATING TABLE Loan
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Loan (
    Loan_Number INT AUTO_INCREMENT PRIMARY KEY,
    Account_Number INT,
    Principal_Amount DECIMAL(10,2),
    Profit_Rate DECIMAL(3,2),
    Time_Period_in_months INT,
    Loan_Type VARCHAR(50),
    Customer_Salary DECIMAL(10,2),
    Final_Amount DECIMAL(10,2),
    Total_Profit DECIMAL(10,2),
    Remaining_Amount DECIMAL(10,2),
    Last_Payment TIMESTAMP
);
''')

# CREATING TABLE Paid_Loans
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Paid_Loans (
        Account_Number INT PRIMARY KEY,
        Principal_Amount Decimal(10,2),
        Profit_Rate Decimal(4,2),
        Time_Period_in_months INT,
        Loan_Type VARCHAR(50),
        Customer_Salary Decimal(10,2),
        Final_Amount Decimal(10,2),
        Total_Profit Decimal(10,2),
        Amount_Unpaid Decimal (10,2),
        Last_Payment TIMESTAMP
    )
''')

#CREATING LIST OF BANK BRANCHES
branches = ["Dubai Mall", "Madinate Badr", "Al Maktoum Branch", "Business Bay", "Abu Al Souq", "Shaikh Zayed Road", "Onyx Tower", "Bur Dubai", "Jumeriah", "DIC", "Al Twar", "Umm Suqeim", "Ibn Battuta Mall", "Oud Meitha", "Al Lisaili", "Muhaisnah Al Ittihad Mall", "Wajaha Maktoom Road", "Mall of the Emirates", "Al Ittihad Mall", "Emirates Headquarters", "Hatta", "Reef Mall", "City Centre Mirdif", "Emirates Cooperative Society Al Twar 3", "Al Nahda", "Abu Dhabi", "Al Salam", "Al Wahda Mall", "Al Muroor", "Bawabat Al Sharq Mall", "Deerfields Mall", "Dalma Mall", "Al Dhafra Mall", "Al Ain", "Al Ain Mall", "Al Jimi", "Al Aliah Mall", "Sharjah", "Wasit Road", "Sharjah Clock Tower", "Al Dhaid", "Al Madam", "Sahara Centre", "Al Qarrayn", "Tasjeel", "Al Zahia City Center", "Kalba", "Ajman", "Al Humaideya", "Ras Al Khaimah", "Khuzam", "Julphar", "Mall of UAQ", "Khor Fakkan", "Fujairah", "Dibba-Fujairah"]

#CREATING LIST OF ACCOUNT TYPES5
account_types = ["Savings Account", "Checking Account", "Escrow Account", "Fixed Deposit", "Al Islami Current Account", "Current Account"]

#main
welcome()


# A FEW PRE CREATED MANAGERS AND EMPLOYEES
print("Manager Mode:")
print("ID-> 1010")
print("PWD-> 1234567")
print()
print("Employee Mode:")
print("ID-> 1011")
print("PWD-> 2345678")
print()
while True:
    try:
        main_menu()
        choice_menu = int(input("ENTER YOUR CHOICE: "))
        print()

        if choice_menu == 1:
            while True:
                manager_id = int(input("Enter Employee ID: "))
                password = int(input("Enter Password: "))
                mycursor.execute("SELECT * FROM employee_details WHERE Employee_ID = %s", (manager_id,))
                employee = mycursor.fetchone()
                if employee[6] == password and employee[9] == 'S':
                    print("Hi", employee[1])
                    main_Manager()
                    break
                else:
                    print("Try Again")
                    break

        elif choice_menu == 2:
            while True:
                employee_id = int(input("Enter Employee ID: "))
                password = int(input("Enter Password: "))
                mycursor.execute("SELECT * FROM employee_details WHERE Employee_ID = %s", (employee_id,))
                employee = mycursor.fetchone()
                if employee[6] == password and employee[9] == 'E':
                    print("Hi", employee[1])
                    main_Employee()
                    break
                else:
                    print("Try Again")
                    break
        elif choice_menu == 0:
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 2.")

    except ValueError:
        print("Invalid input. Please enter a valid integer.")

#making a change
print("Nothing Much")
