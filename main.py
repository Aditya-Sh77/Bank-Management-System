import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

# Utility Functions

def hash_password(password):
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_database():
    """Initializes the SQLite database."""
    conn = sqlite3.connect('bank_system.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        balance REAL DEFAULT 0.0,
                        age INTEGER,
                        gender TEXT,
                        mobile INTEGER,
                        address TEXT,
                        district TEXT,
                        pincode INTEGER,
                        state TEXT,
                        country TEXT,
                        nominee TEXT,
                        kyc_status TEXT DEFAULT 'false',
                        loan_status TEXT DEFAULT 'false',
                        loan_type TEXT,
                        loan_amount REAL DEFAULT 0.0,
                        loan_duration INTEGER,
                        insurance_status TEXT DEFAULT 'false'
                      )''')
    conn.commit()
    conn.close()

# GUI Application

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("400x600")

        self.initialize_home_screen()

    def initialize_home_screen(self):
        """Displays the home screen with Login and Register options."""
        self.clear_screen()

        tk.Label(self.root, text="Bank Management System", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Login", width=15, command=self.show_login_screen).pack(pady=10)
        tk.Button(self.root, text="Register", width=15, command=self.show_register_screen).pack(pady=10)

    def show_login_screen(self):
        """Displays the login screen."""
        self.clear_screen()

        tk.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        def login():
            username = username_entry.get()
            password = hash_password(password_entry.get())

            conn = sqlite3.connect('bank_system.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password))
            account = cursor.fetchone()
            conn.close()

            if account:
                messagebox.showinfo("Login Successful", f"Welcome, {account[1]}!")
                self.show_dashboard(account)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        tk.Button(self.root, text="Login", command=login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.initialize_home_screen).pack(pady=10)

    def show_register_screen(self):
        """Displays the registration screen."""
        self.clear_screen()

        tk.Label(self.root, text="Register", font=("Arial", 18)).pack(pady=10)

        entries = {}
        fields = ["Name", "Username", "Password", "Initial Deposit", "Age", "Gender", "Mobile", "Address", "District", "Pincode", "State", "Country", "Nominee"]

        for field in fields:
            tk.Label(self.root, text=f"{field}:").pack()
            entry = tk.Entry(self.root)
            entry.pack(pady=5)
            entries[field] = entry

        def register():
            data = {field: entries[field].get() for field in fields}
            try:
                conn = sqlite3.connect('bank_system.db')
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO accounts (name, username, password, balance, age, gender, mobile, address, district, pincode, state, country, nominee)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (data["Name"], data["Username"], hash_password(data["Password"]), float(data["Initial Deposit"]),
                                int(data["Age"]), data["Gender"], int(data["Mobile"]), data["Address"], data["District"],
                                int(data["Pincode"]), data["State"], data["Country"], data["Nominee"]))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Account registered successfully!")
                self.initialize_home_screen()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")

        tk.Button(self.root, text="Register", command=register).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.initialize_home_screen).pack(pady=10)

    def show_dashboard(self, account):
        """Displays the dashboard for a logged-in user."""
        self.clear_screen()

        tk.Label(self.root, text=f"Welcome, {account[1]}!", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text=f"Balance: ${account[4]:.2f}", font=("Arial", 16)).pack(pady=10)

        def deposit():
            amount = float(amount_entry.get())
            new_balance = account[4] + amount

            conn = sqlite3.connect('bank_system.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE accounts SET balance = ? WHERE id = ?', (new_balance, account[0]))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Deposited ${amount:.2f}. Updated balance: ${new_balance:.2f}")
            account[4] = new_balance

        def withdraw():
            amount = float(amount_entry.get())
            if amount > account[4]:
                messagebox.showerror("Error", "Insufficient balance.")
                return

            new_balance = account[4] - amount

            conn = sqlite3.connect('bank_system.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE accounts SET balance = ? WHERE id = ?', (new_balance, account[0]))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Withdrew ${amount:.2f}. Updated balance: ${new_balance:.2f}")
            account[4] = new_balance

        def apply_kyc():
            conn = sqlite3.connect('bank_system.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE accounts SET kyc_status = "true" WHERE id = ?', (account[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "KYC completed successfully!")

        def request_loan():
            loan_amount = float(loan_entry.get())
            loan_duration = int(duration_entry.get())
            conn = sqlite3.connect('bank_system.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE accounts SET loan_status = "true", loan_amount = ?, loan_duration = ? WHERE id = ?''',
                           (loan_amount, loan_duration, account[0]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Loan of ${loan_amount:.2f} approved for {loan_duration} months.")

        tk.Label(self.root, text="Enter Amount:").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack(pady=5)

        tk.Button(self.root, text="Deposit", command=deposit).pack(pady=5)
        tk.Button(self.root, text="Withdraw", command=withdraw).pack(pady=5)

        tk.Label(self.root, text="KYC Application:").pack(pady=10)
        tk.Button(self.root, text="Apply KYC", command=apply_kyc).pack(pady=5)

        tk.Label(self.root, text="Loan Request:").pack(pady=10)
        tk.Label(self.root, text="Loan Amount:").pack()
        loan_entry = tk.Entry(self.root)
        loan_entry.pack(pady=5)
        tk.Label(self.root, text="Loan Duration (months):").pack()
        duration_entry = tk.Entry(self.root)
        duration_entry.pack(pady=5)
        tk.Button(self.root, text="Request Loan", command=request_loan).pack(pady=10)

        tk.Button(self.root, text="Logout", command=self.initialize_home_screen).pack(pady=10)

    def clear_screen(self):
        """Clears all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Initialize the application
initialize_database()
root = tk.Tk()
app = BankApp(root)
root.mainloop()
