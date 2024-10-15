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
from prettytable import PrettyTable

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
            elif account_holder_name.isdigit():
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

def account_modificator(Account_Number):
    try:
        mycursor.execute("SELECT * FROM accounts WHERE Account_Number = {}".format(Account_Number))
        Existing_Account = mycursor.fetchone()

        if Existing_Account is None:
            print("Account not found.")
            return

        search_account_details(Account_Number)

        while True:
            print('''
            What Details Do you want to change?
            Enter 1 to change Name
            Enter 2 to change Age
            Enter 3 to change Account Type
            Enter 4 to Transfer to a different Branch
            Enter 5 to change PIN
            Enter 0 if you don't want any more changes
            ''')

            choicetochange = int(input("Enter your Choice here: "))

            if choicetochange == 0:
                return
            elif choicetochange == 1:
                new_account_holder_name = input("Enter New account holder Name: ")
                if new_account_holder_name == '00':
                    return
                elif not new_account_holder_name.isalpha():
                    print("Name must be a string value")
                    continue
                else:
                    mycursor.execute("UPDATE accounts SET account_holder_name = '{}' WHERE account_number = {}".format(new_account_holder_name, Account_Number))
                    mydb.commit()
            elif choicetochange == 2:
                new_account_holder_age = int(input("Enter New account holder Age: "))
                if new_account_holder_age == 00 or new_account_holder_age < 18 or new_account_holder_age > 100:
                    return
                mycursor.execute("UPDATE accounts SET age = {} WHERE account_number = {}".format(new_account_holder_age, Account_Number))
                mydb.commit()
            elif choicetochange == 3:
                new_account_type = input("Enter the new Account Type: ")
                if new_account_type == '00' or new_account_type not in account_types:
                    return
                mycursor.execute("UPDATE accounts SET account_type = '{}' WHERE account_number = {}".format(new_account_type, Account_Number))
                mydb.commit()
            elif choicetochange == 4:
                new_account_branch = input("Enter the name of the new branch: ")
                if new_account_branch == '00' or new_account_branch not in branches:
                    return
                mycursor.execute("UPDATE accounts SET branch_name = '{}' WHERE account_number = {}".format(new_account_branch, Account_Number))
                mydb.commit()
            elif choicetochange == 5:
                new_pin = input("Enter the new 7-digit PIN: ")
                if new_pin == '00' or not new_pin.isdigit() or len(new_pin) != 7:
                    print("Invalid PIN. Please enter a 7-digit numeric PIN.")
                    continue
                mycursor.execute("UPDATE accounts SET pin = {} WHERE account_number = {}".format(new_pin, Account_Number))
                mydb.commit()
            else:
                print("Please Enter a valid choice")

            print("Details updated successfully.")
            print("Updated details:")
            search_account_details(Account_Number)
    except ValueError:
        print("Invalid input. Please enter a valid numeric choice.")

def account_deleter(account_number):
    if account_number == 00:
        return
    
    mycursor.execute("SELECT * FROM Loan WHERE Account_Number = %s", (account_number,))
    existing_loan = mycursor.fetchone()

    if existing_loan:
        print("Cannot delete the account. It has a loan pending.")
        return

    mycursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
    existing_account = mycursor.fetchone()

    if existing_account is None:
        print("Account not found.")
        return

    print("Existing details:")
    search_account_details(account_number)

    confirmation = input(f"Do you want to delete the account with number {account_number}? (yes/no): ").lower()

    if confirmation == "yes":
        mycursor.execute("""
            INSERT INTO deleted_accounts
            (account_number, pin, account_holder_name, age, balance, date_registered, account_type, branch_name, last_transaction_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            existing_account[0],  
            existing_account[1],  
            existing_account[2], 
            existing_account[3], 
            existing_account[4], 
            existing_account[5],  
            existing_account[6], 
            existing_account[7], 
            existing_account[8], 
))

        mycursor.execute("DELETE FROM accounts WHERE account_number = %s", (account_number,))
        mydb.commit()

        print("Account deleted successfully.")
        print("Updated details:")
        search_account_details(account_number)
    else:
        print("Account deletion canceled.")


def display_deleted_accounts():
    mycursor.execute("SELECT * FROM deleted_accounts")
    rows = mycursor.fetchall()
    if not rows:
        print("No deleted accounts found.")
    else:
        table = PrettyTable()
        table.field_names = ["Account Number", "PIN", "Account Holder Name", "Age", "Balance", "Date Registered", "Account Type", "Branch Name", "Last Transaction Date"]
        for row in rows:
            table.add_row(row)
        print("Deleted Accounts:")
        print(table)

def transaction_displayer():
    mycursor.execute("SELECT * FROM Transactions")
    rows = mycursor.fetchall()
    if not rows:
        print("No records found.")
    else:
        table = PrettyTable()
        table.field_names = ["Account Number", "Receiving Account Number", "Transaction Time",
                             "Transaction Amount", "Transaction Number"]
        for row in rows:
            table.add_row([row[0], row[1], row[2], row[3], row[4]])
        print("Transaction Details:")
        print(table)
            
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

def grant_loan(account_number):
    mycursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(account_number))
    existing_account = mycursor.fetchone()
    if existing_account is None:
        print("Account not found.")
        return
    while True:
        try:
            principal_amount = Decimal(input("Enter loan amount: "))
            if principal_amount > 0:
                break
            else:
                print("Loan amount must be greater than 0. Please enter a valid value.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for loan amount.")

    while True:
        try:
            profit_rate = float(input("Enter profit rate: "))
            if 0 <= profit_rate <= 100:  
                break
            else:
                print("Profit rate must be between 0 and 100. Please enter a valid value.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for profit rate.")
    while True:
        try:
            time_period_in_months = int(input("Enter time period of loan in months: "))
            if time_period_in_months > 0:
                break
            else:
                print("Time period must be greater than 0. Please enter a valid value.")
        except ValueError:
            print("Invalid input. Please enter an integer value for time period.")
    loan_type = input("Enter loan type: ")
    while True:
        try:
            customer_salary = float(input("Enter customer salary: "))
            if customer_salary > 0:
                break
            else:
                print("Customer salary must be greater than 0. Please enter a valid value.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for customer salary.")
    final_amount = float(principal_amount) * ((1 + profit_rate / 100) ** (time_period_in_months / 12))
    if principal_amount > customer_salary * time_period_in_months:
        print("Principal amount exceeds the allowed limit based on salary and time period.")
        return
    new_balance = existing_account[3] + Decimal(principal_amount)
    mycursor.execute("""
        UPDATE accounts
        SET balance = {},
            last_transaction_date = NOW()
        WHERE account_number = {}
    """.format(new_balance, account_number))
    total_profit = final_amount - float(principal_amount)
    mycursor.execute("""
    INSERT INTO Loan
    (Account_Number, Principal_Amount, Profit_Rate, Time_Period_in_months, Loan_Type, Customer_Salary, Final_Amount, Total_Profit, Remaining_Amount, Last_Payment)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (account_number, principal_amount, profit_rate, time_period_in_months, loan_type, customer_salary, final_amount, total_profit, principal_amount, None))

    mydb.commit()
    print("Loan added successfully.")

        
def loans_displayer():
    mycursor.execute("SELECT * FROM Loan")
    rows = mycursor.fetchall()
    if not rows:
        print("No loan records found.")
    else:
        table = PrettyTable()
        table.field_names = ["Loan Number", "Account Number", "Principal Amount", "Profit Rate", "Time Period (Months)", 
                             "Loan Type", "Customer Salary", "Final Amount", "Total Profit", "Remaining Amount", "Last Payment Date"]
        for row in rows:
            table.add_row(row)
        print("Loan Details:")
        print(table)


def loan_details_displayer(account_number):
    if account_number == 00:
        return
    mycursor.execute("SELECT * FROM Loan WHERE Account_Number = {}".format(account_number))
    loan_details = mycursor.fetchone()
    if loan_details:
        print("Loan Details for Account Number {}:".format(account_number))
        print("Loan Number: {}".format(loan_details[0]))
        print("Principal Amount: {}".format(loan_details[2]))
        print("Profit Rate: {}".format(loan_details[3]))
        print("Time Period in Months: {}".format(loan_details[4]))
        print("Loan Type: {}".format(loan_details[5]))
        print("Customer Salary: {}".format(loan_details[6]))
        print("Final Amount: {}".format(loan_details[7]))
        print("Total Profit: {}".format(loan_details[8]))
        print("Remaining Amount for Payment: {}".format(loan_details[9]))
        print("Last Payment: {}".format(loan_details[10]))
    else:
        print("No loan details found for Account Number {}.".format(account_number))

def loan_modifier(Account_Number):
    if Account_Number == 00:
        return
    mycursor.execute("SELECT * FROM Loan WHERE Account_Number = {}".format(Account_Number))
    existing_loan = mycursor.fetchone()
    if existing_loan is None:
        print("Loan not found.")
        return
    loan_details_displayer(Account_Number)
    principal_amount = existing_loan[2]
    profit_rate = existing_loan[3]
    time_period = existing_loan[4]
    while True:
        print('''
        What Details Do u want to change?
        Enter 1 to change Profit Rate
        Enter 2 to change Time Period (in months)
        Enter 3 to change Customer Salary
        Enter 0 if u dont want any more changes
        ''')
        choicetochange = int(input("Enter your Choice here: "))
        if choicetochange == 0:
            return
        elif choicetochange == 1:
            new_profit_rate = float(input("Enter New Profit Rate: "))
            if new_profit_rate == 00:
                return
            else:
                new_final_amount = float(principal_amount) * (1 + new_profit_rate/100)**(time_period)
                mycursor.execute('''UPDATE Loan SET Profit_Rate = {},
                                 Final_Amount = {}
                                 WHERE Account_Number = {}'''.format(new_profit_rate, new_final_amount, Account_Number))        
                mydb.commit()
        elif choicetochange == 2:
            new_time_period = int(input("Enter New Time Period (in months): "))
            if new_time_period == 00:
                return
            else:
                new_final_amount = principal_amount * (1 + profit_rate/100)**(new_time_period)
                mycursor.execute('''UPDATE Loan SET Time_Period_in_months = {},
                                 Final_Amount = {} WHERE Account_Number = {}'''.format(new_time_period, new_final_amount, Account_Number))
                mydb.commit()
        elif choicetochange == 3:
            new_customer_salary = float(input("Enter the new Salary: "))
            if new_customer_salary == 00:
                return
            elif principal_amount > new_customer_salary * time_period:
                print("Principal amount exceeds the allowed limit based on salary and time period.")
                return
            else:
                mycursor.execute("UPDATE Loan SET Customer_Salary = {} WHERE Account_Number = {}".format(new_customer_salary, Account_Number))
                mydb.commit()
        else:
            print("Please Enter a valid choice")
            
    print("Loan details updated successfully.")
    loan_details_displayer(Account_Number)
    
def loan_deleter(account_number):
    if account_number == 0:
        return
    mycursor.execute("SELECT * FROM Loan WHERE Account_Number = %s", (account_number,))
    existing_loan = mycursor.fetchone()
    if existing_loan is None:
        print("No loan found for the account.")
        return
    loan_details_displayer(account_number)
    confirmation = input("Do you want to write off the loan for account {}? (yes/no): ".format(account_number)).lower()
    if confirmation == "yes": 
        mycursor.execute("""
            INSERT INTO Paid_Loans
            (Loan_Number, Account_Number, Principal_Amount, Profit_Rate, Time_Period_in_months, Loan_Type, Customer_Salary, Final_Amount, Total_Profit, Amount_Unpaid, Last_Payment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (existing_loan[0], existing_loan[1], existing_loan[2], existing_loan[3], existing_loan[4],
              existing_loan[5], existing_loan[6], existing_loan[7], existing_loan[8], existing_loan[9]))
        
        mycursor.execute("DELETE FROM Loan WHERE Account_Number = %s", (account_number,))
        mydb.commit()
        
        print("Loan successfully written off.")
    else:
        print("Loan write-off canceled.")

def display_paid_loans():
    mycursor.execute("SELECT * FROM Paid_Loans")
    rows = mycursor.fetchall()
    if not rows:
        print("No paid loans found.")
    else:
        table = PrettyTable()
        table.field_names = ["Account Number", "Principal Amount", "Profit Rate", "Time Period (Months)", 
                             "Loan Type", "Customer Salary", "Final Amount", "Total Profit", "Amount Unpaid", "Last Payment Date"]
        for row in rows:
            table.add_row(row)
        print("Paid Loans Details:")
        print(table)

def employee_displayer():
    tables = ["employee_details", "employee_salaries"]

    for table_name in tables:
        mycursor.execute(f"SELECT * FROM {table_name}")
        rows = mycursor.fetchall()

        if not rows:
            print(f"No records found in {table_name}.")
        else:
            table = PrettyTable()
            if table_name == "employee_details":
                field_names = ["Employee_ID", "First_Name", "Last_Name", "Date_of_Birth", "Gender", "Phone_Number", "Department", "Job_Title", "Clearance_Level", "Date_of_Joining"]
            elif table_name == "employee_salaries":
                field_names = ["Salary_ID", "Employee_ID", "Salary", "Payment_Date"]
            else:
                print(f"Unsupported table: {table_name}")
                continue

            for field_name in field_names:
                table.field_names.append(field_name)

            for row in rows:
                table.add_row(row)

            print(f"{table_name.capitalize()}:")
            print(table)
        
def employee_details_displayer(employee_id):
    if employee_id == 00:
        return
    
    # Display details from employee_details table
    mycursor.execute("SELECT * FROM employee_details WHERE Employee_ID = %s", (employee_id,))
    employee_details = mycursor.fetchone()

    if employee_details:
        print("Employee Details:")
        print("Employee ID: {}".format(employee_details[0]))
        print("First Name: {}".format(employee_details[1]))
        print("Last Name: {}".format(employee_details[2]))
        print("Date of Birth: {}".format(employee_details[3]))
        print("Gender: {}".format(employee_details[4]))
        print("Phone Number: {}".format(employee_details[5]))
        print("Password: {}".format(employee_details[6]))
        print("Department: {}".format(employee_details[7]))
        print("Job Title: {}".format(employee_details[8]))
        print("Clearance Level: {}".format(employee_details[9]))
        print("Date of Joining: {}".format(employee_details[10]))
        mycursor.execute("SELECT * FROM employee_salaries WHERE Employee_ID = %s", (employee_id,))
        employee_salary_details = mycursor.fetchone()

        if employee_salary_details:
            print("\nEmployee Salary Details:")
            print("Salary ID: {}".format(employee_salary_details[0]))
            print("Salary: {}".format(employee_salary_details[2]))
            print("Payment Date: {}".format(employee_salary_details[3]))
        else:
            print("\nNo salary details found.")
    else:
        print("No employee details found for Employee ID {}.".format(employee_id))
    
def new_employee():
    while True:
        first_name = input("Enter First Name: ")
        if first_name == '00':
            return
        last_name = input("Enter Last Name: ")
        if last_name == '00':
            return
        date_of_birth = input("Enter Date of Birth (YYYY-MM-DD): ")
        if date_of_birth == '00':
            return
        gender = input("Enter Gender (M/F): ")
        if gender == '00':
            return
        
        while True:
            try:
                phone_number = input("Enter Phone Number (05X XXX XXXX): ")
                if phone_number == '00':
                    return
                elif not (phone_number.startswith("05") and len(phone_number) == 10):
                    raise ValueError("Invalid phone number format. Please enter again.")
                break
            except ValueError as e:
                print(e)
        department = input("Enter Department: ")
        if department == '00':
            return
        job_title = input("Enter Job Title: ")
        if job_title == '00':
            return
        clearance_level = input("Enter Clearance Level (E/S): ")
        if clearance_level == '00':
            return
        mycursor.execute("""
            INSERT INTO employee_details
            (First_Name, Last_Name, Date_of_Birth, Gender, Phone_Number, Department, Job_Title, Clearance_Level, Date_of_Joining)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE)
        """, (first_name, last_name, date_of_birth, gender, phone_number, department, job_title, clearance_level))
        mycursor.execute("SELECT LAST_INSERT_ID()")
        employee_id = mycursor.fetchone()[0]
        payment_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        while True:
            try:
                salary = Decimal(input("Enter Salary (per month): "))
                if salary == 00:
                    return
                elif salary < 0:
                    raise ValueError("Salary must be a non-negative value. Please enter again.")
                break
            except ValueError as e:
                print(e)

        mycursor.execute("""
            INSERT INTO employee_salaries (Employee_ID, Salary, Payment_Date)
            VALUES (%s, %s, %s)
        """, (employee_id, salary, payment_date))
        mydb.commit()
        print("New employee added successfully.")
        break
    
def employee_deleter(employee_id):
    if employee_id == '00':
        return
    
    mycursor.execute("SELECT * FROM employee_details WHERE Employee_ID = %s", (employee_id,))
    existing_employee = mycursor.fetchone()
    if existing_employee is None:
        print("Employee not found.")
        return

    print("Existing details:")
    employee_details_displayer(employee_id)
    confirmation = input(f"Do you want to delete the employee with Employee_ID {employee_id}? (yes/no): ").lower()
    if confirmation == "yes":
        mycursor.execute("DELETE FROM employee_salaries WHERE Employee_ID = %s", (employee_id,))
        mycursor.execute("DELETE FROM employee_details WHERE Employee_ID = %s", (employee_id,))
        mydb.commit()
        print("Employee deleted successfully.")
        print("Updated employee details:")
        employee_details_displayer(employee_id)
    else:
        print("Employee deletion canceled.")

def employee_details_modifier(employee_id):
    if employee_id == 00:
        return
    
    mycursor.execute("SELECT * FROM employee_details WHERE Employee_ID = {}".format(employee_id))
    existing_employee = mycursor.fetchone()

    if existing_employee is None:
        print("Employee not found.")
        return

    employee_details_displayer(employee_id)
    
    while True:
        print('''
        What Details Do u want to change?
        Enter 1 to change Name
        Enter 2 to change Phone Number
        Enter 3 to change Department
        Enter 4 to change Job Title
        Enter 5 to change Clearance Level
        Enter 6 to chnage Password
        Enter 0 if u dont want any more changes
        ''')

        choicetochange = int(input("Enter your Choice here: "))

        if choicetochange == 0:
            return
        elif choicetochange == 1:
            new_name = input("Enter New Name (First Name Last Name): ")
            if new_name == '00':
                return
            names = new_name.split()
            if len(names) != 2:
                print("Invalid input for Name. Please enter only/both First Name and Last Name.")
                continue
            new_first_name, new_last_name = names[0], names[1]
            mycursor.execute("UPDATE employee_details SET First_Name = '{}', Last_Name = '{}' WHERE Employee_ID = {}".format(new_first_name, new_last_name, employee_id))
            mydb.commit()
        elif choicetochange == 2:
            while True:
                try:
                    new_phone_number = input("Enter New Phone Number (05X XXX XXXX): ")
                    if new_phone_number == '00':
                        return
                    elif not (new_phone_number.startswith("05") and len(new_phone_number) == 10):
                        raise ValueError("Invalid phone number format. Please enter again.")
                    break
                except ValueError as e:
                    print(e)
                mycursor.execute("UPDATE employee_details SET Phone_Number = '{}' WHERE Employee_ID = {}".format(new_phone_number, employee_id))
                mydb.commit()
        elif choicetochange == 3:
            new_department = input("Enter New Department: ")
            if new_department == '00':
                return
            mycursor.execute("UPDATE employee_details SET Department = '{}' WHERE Employee_ID = {}".format(new_department, employee_id))
            mydb.commit()
        elif choicetochange == 4:
            new_job_title = input("Enter New Job Title: ")
            if new_job_title == '00':
                return
            mycursor.execute("UPDATE employee_details SET Job_Title = '{}' WHERE Employee_ID = {}".format(new_job_title, employee_id))
            mydb.commit()
        elif choicetochange == 5:
            new_clearance_level = input("Enter New Clearance Level: ")
            if new_clearance_level == '00':
                return
            mycursor.execute("UPDATE employee_details SET Clearance_Level = '{}' WHERE Employee_ID = {}".format(new_clearance_level, employee_id))
            mydb.commit()
        elif choicetochange == 6:
            new_password = int(input("Enter New Password: "))
            if new_password == '00':
                return
            elif len(str(new_password)) != 7:
                print("Invalid PIN. Please enter a 7-digit PIN.")
                continue
            mycursor.execute("UPDATE employee_details SET Password = {} WHERE Employee_ID = {}".format(new_password, employee_id))
            mydb.commit()
        else:
            print("Please Enter a valid choice")

    print("Details updated successfully.")
    print("Updated details:")
    employee_details_displayer()
