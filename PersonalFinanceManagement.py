import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Toplevel, ttk
from datetime import datetime

def initialize_db():
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0]
    else:
        messagebox.showerror("Error", "Invalid credentials.")
        return None


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")  
        self.root.title("Personal Finance Manager")
        self.current_user = None

        self.login_frame = Toplevel(self.root)
        self.login_frame.geometry("400x300") 
        self.login_frame.title("Login")
        self.login_username = StringVar()
        self.login_password = StringVar()

        Label(self.login_frame, text="Username:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        Entry(self.login_frame, textvariable=self.login_username, font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=10)
        Label(self.login_frame, text="Password:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
        Entry(self.login_frame, textvariable=self.login_password, show="*", font=("Arial", 14)).grid(row=1, column=1, padx=10, pady=10)

        Button(self.login_frame, text="Login", font=("Arial", 14), command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        Button(self.login_frame, text="Register", font=("Arial", 14), command=self.open_register_window).grid(row=3, column=0, columnspan=2, pady=10)

        
        self.main_frame = None

    def open_register_window(self):
        register_window = Toplevel(self.root)
        register_window.geometry("400x300")  
        register_window.title("Register")

        reg_username = StringVar()
        reg_password = StringVar()

        Label(register_window, text="Username:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        Entry(register_window, textvariable=reg_username, font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=10)
        Label(register_window, text="Password:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
        Entry(register_window, textvariable=reg_password, show="*", font=("Arial", 14)).grid(row=1, column=1, padx=10, pady=10)

        Button(register_window, text="Register", font=("Arial", 14),
               command=lambda: register_user(reg_username.get(), reg_password.get())).grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        user_id = login_user(username, password)
        if user_id:
            self.current_user = user_id
            self.login_frame.destroy()
            self.show_main_screen()

    def show_main_screen(self):
        self.main_frame = Toplevel(self.root)
        self.main_frame.geometry("800x600") 
        self.main_frame.title("Main Menu")

        Button(self.main_frame, text="Add Transaction", font=("Arial", 14), command=self.add_transaction_window).pack(pady=10)
        Button(self.main_frame, text="View Transactions", font=("Arial", 14), command=self.view_transactions_window).pack(pady=10)
        Button(self.main_frame, text="Generate Report", font=("Arial", 14), command=self.generate_report_window).pack(pady=10)
        Button(self.main_frame, text="Logout", font=("Arial", 14), command=self.logout).pack(pady=10)

    def add_transaction_window(self):
        transaction_window = Toplevel(self.root)
        transaction_window.geometry("500x400")  
        transaction_window.title("Add Transaction")

        trans_type = StringVar()
        trans_category = StringVar()
        trans_amount = StringVar()

        Label(transaction_window, text="Type (Income/Expense):", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        Entry(transaction_window, textvariable=trans_type, font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=10)
        Label(transaction_window, text="Category:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
        Entry(transaction_window, textvariable=trans_category, font=("Arial", 14)).grid(row=1, column=1, padx=10, pady=10)
        Label(transaction_window, text="Amount:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10)
        Entry(transaction_window, textvariable=trans_amount, font=("Arial", 14)).grid(row=2, column=1, padx=10, pady=10)

        Button(transaction_window, text="Add", font=("Arial", 14), 
               command=lambda: self.add_transaction(trans_type.get(), trans_category.get(), trans_amount.get(), transaction_window)).grid(row=3, column=0, columnspan=2, pady=10)

    def add_transaction(self, t_type, category, amount, window):
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO transactions (user_id, type, category, amount, date) 
                              VALUES (?, ?, ?, ?, ?)''', (self.current_user, t_type, category, float(amount), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            messagebox.showinfo("Success", "Transaction added successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def view_transactions_window(self):
        view_window = Toplevel(self.root)
        view_window.geometry("800x600")  
        view_window.title("View Transactions")

        tree = ttk.Treeview(view_window, columns=("Type", "Category", "Amount", "Date"), show="headings")
        tree.heading("Type", text="Type")
        tree.heading("Category", text="Category")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")
        tree.pack(fill="both", expand=True)

        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT type, category, amount, date FROM transactions WHERE user_id = ?', (self.current_user,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def generate_report_window(self):
        report_window = Toplevel(self.root)
        report_window.geometry("500x400")
        report_window.title("Financial Report")

        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT type, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY type''', (self.current_user,))
        report = cursor.fetchall()
        conn.close()

        total_income = sum([r[1] for r in report if r[0] == 'Income'])
        total_expense = sum([r[1] for r in report if r[0] == 'Expense'])
        savings = total_income - total_expense

        Label(report_window, text=f"Total Income: {total_income}", font=("Arial", 14)).pack(pady=10)
        Label(report_window, text=f"Total Expense: {total_expense}", font=("Arial", 14)).pack(pady=10)
        Label(report_window, text=f"Savings: {savings}", font=("Arial", 14)).pack(pady=10)

    def logout(self):
        self.main_frame.destroy()
        self.current_user = None
        self.login_frame = Toplevel(self.root)
        self.__init__(self.root)

if __name__ == "__main__":
    initialize_db()
    root = Tk()
    root.withdraw()  
    app = FinanceApp(root)
    root.mainloop()
