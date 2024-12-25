Personal Finance Management Application

Overview

This is a Personal Finance Management application built using Python and the Tkinter library for the graphical user interface (GUI). The application allows users to register, log in, manage their income and expenses, view transactions, and generate financial reports.

Features

User Registration and Authentication

Users can register with a unique username and password.

Users can log in with their credentials to access the application.

Transaction Management

Add transactions with details such as type (Income/Expense), category, and amount.

View all transactions in a tabular format.

Financial Reports

Generate financial reports to view total income, total expenses, and savings.

Database Persistence

Data is stored in a SQLite database (finance_manager.db) to ensure persistence across sessions.

Usage

Run the Application:

Navigate to the directory containing the script.

Execute the script using the command:

python personal_finance_app.py

Register:

On the login window, click on the "Register" button to create a new account.

Enter a unique username and password, then click "Register."

Log In:

Enter your username and password, then click "Login."

Add Transactions:

After logging in, click on "Add Transaction."

Fill in the type (Income/Expense), category, and amount, then click "Add."

View Transactions:

Click on "View Transactions" to see all your transactions in a tabular format.

Generate Reports:

Click on "Generate Report" to view your total income, expenses, and savings.

Logout:

Click on "Logout" to return to the login screen.

Database Details

Users Table:

id: Primary key

username: Unique username

password: User password

Transactions Table:

id: Primary key

user_id: Foreign key referencing the user

type: Income or Expense

category: Transaction category

amount: Numerical value

date: Date and time of transaction
