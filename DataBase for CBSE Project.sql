CREATE database bank;
use bank;

CREATE TABLE employee_details (
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
    Date_of_Joining DATE) AUTO_INCREMENT = 1000;
drop table employee_details;
CREATE TABLE employee_salaries (
    Salary_ID INT AUTO_INCREMENT PRIMARY KEY,
    Employee_ID INT,
    Salary DECIMAL(10, 2),
    Payment_Date DATE,
    CONSTRAINT fk_employee_salaries_employee_id 
        FOREIGN KEY (Employee_ID) 
        REFERENCES employee_details(Employee_ID)
);
drop table employee_salaries;
CREATE TABLE accounts (
	account_number INT AUTO_INCREMENT PRIMARY KEY,
    pin INT(8),
    account_holder_name VARCHAR(255),
    age INT,
    balance DECIMAL(10, 2),
    date_registered DATE,
    account_type VARCHAR(50),
    branch_name VARCHAR(100),
    last_transaction_date TIMESTAMP) AUTO_INCREMENT = 1000000000;

CREATE TABLE IF NOT EXISTS deleted_accounts (
	account_number INT AUTO_INCREMENT PRIMARY KEY,
    pin INT(8),
	account_holder_name VARCHAR(255),
    age INT,
	balance DECIMAL(10, 2),
	date_registered DATE,
	account_type VARCHAR(50),
	branch_name VARCHAR(100),
	last_transaction_date TIMESTAMP) AUTO_INCREMENT = 1000000000;
    
CREATE TABLE IF NOT EXISTS Transactions (
	Account_Number INT,
	Reciving_Account_Number INT,
	Transaction_Time TIMESTAMP,
	Transaction_Amount Decimal(10,2),
	Transaction_Number INT AUTO_INCREMENT PRIMARY KEY);


CREATE TABLE IF NOT EXISTS Loan (
	Loan_Number INT auto_increment PRIMARY KEY,
	Account_Number INT,
	Principal_Amount Decimal(10,2),
	Profit_Rate Decimal(3,2),
    Time_Period_in_months INT,
    Loan_Type VARCHAR(50),
    Customer_Salary Decimal(10,2),
    Final_Amount Decimal(10,2),
    Total_Profit Decimal(10,2),
    Remaining_Amount Decimal (10,2),
    Last_Payment TIMESTAMP);

CREATE TABLE IF NOT EXISTS Paid_Loans (
	Loan_Number INT PRIMARY KEY,
	Account_Number INT,
    Principal_Amount Decimal(10,2),
    Profit_Rate Decimal(4,2),
    Time_Period_in_months INT,
    Loan_Type VARCHAR(50),
    Customer_Salary Decimal(10,2),
    Final_Amount Decimal(10,2),
    Total_Profit Decimal(10,2),
    Amount_Unpaid Decimal (10,2),
    Last_Payment TIMESTAMP);


select * from employee_details;
drop table employee_details; 

select * from employee_salaries;
drop table employee_salaries;

select * from accounts;
DELETE FROM accounts
WHERE account_number > 1000000019;

INSERT INTO employee_details (First_Name, Last_Name, Date_of_Birth, Gender, Phone_Number, Password, Department, Job_Title, Clearance_Level, Date_of_Joining)
VALUES 
    ('Humaid', 'Mohammed', '1990-05-15', 'M', '05123456789', '1234567', 'IT', 'Software Engineer', 'S', '2022-01-15'),
    ('Richi', 'Kumar', '1985-08-22', 'F', '05234567890', '2345678', 'HR', 'HR Manager', 'E', '2022-02-01'),
    ('Roy', 'Harwani', '1995-11-10', 'M', '05345678901', '3456789', 'Finance', 'Accountant', 'E', '2022-03-10'),
    ('Emma', 'Watson', '1992-07-18', 'F', '05456789012', '4567890', 'Marketing', 'Marketing Specialist', 'S', '2022-04-20'),
    ('Lionel', 'Messi', '1988-04-25', 'M', '05567890123', '5678901', 'Sales', 'Sales Manager', 'S', '2022-05-12');

INSERT INTO employee_salaries (Employee_ID, Salary, Payment_Date)
VALUES 
    (1010, 5000.00, '2023-12-31'),
    (1011, 6000.00, '2024-01-01'),
    (1012, 5500.00, '2024-01-10'),
    (1013, 4800.00, '2024-01-13'),
    (1014, 7000.00, '2024-01-16');

select * from Transactions;

INSERT INTO accounts (pin, account_holder_name, age, balance, date_registered, account_type, branch_name, last_transaction_date)
VALUES 
    (12345678, 'Amit Patel', 30, 5000.00, '2023-01-01', 'Savings', 'Main Branch', '2023-12-31 12:30:00'),
    (87654321, 'Priya Sharma', 25, 7000.00, '2023-02-15', 'Checking', 'Downtown Branch', '2023-12-31 15:45:00'),
    (65432178, 'Rahul Kapoor', 35, 12000.00, '2023-03-10', 'Savings', 'West Branch', '2023-12-31 09:15:00'),
    (98761234, 'Neha Desai', 28, 9000.00, '2023-04-20', 'Checking', 'East Branch', '2023-12-31 18:20:00'),
    (45678901, 'Vikram Singh', 40, 15000.00, '2023-05-05', 'Savings', 'North Branch', '2023-12-31 14:00:00');

INSERT INTO accounts (pin, account_holder_name, age, balance, date_registered, account_type, branch_name, last_transaction_date)
VALUES 
    (56789012, 'Anjali Joshi', 22, 3000.00, '2023-06-12', 'Savings', 'South Branch', '2023-12-31 10:45:00'),
    (34561278, 'Suresh Gupta', 45, 18000.00, '2023-07-25', 'Checking', 'Main Branch', '2023-12-31 16:30:00'),
    (89012345, 'Pooja Verma', 32, 10000.00, '2023-08-10', 'Savings', 'Downtown Branch', '2023-12-31 11:20:00'),
    (12347890, 'Rajesh Singh', 28, 6000.00, '2023-09-18', 'Checking', 'West Branch', '2023-12-31 14:55:00'),
    (23456789, 'Meera Khanna', 35, 13000.00, '2023-10-03', 'Savings', 'East Branch', '2023-12-31 09:10:00');

select * from accounts;

select * from Loan;
drop table Loan