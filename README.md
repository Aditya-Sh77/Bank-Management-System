# Bank Management System

## Overview
This project is a simple **Bank Management System** built using Python and Tkinter for the GUI and SQLite for the database. The application allows users to register, log in, and perform various banking operations such as deposits, withdrawals, applying for KYC, and requesting loans.

## Features
- **User Registration and Login**
- **Secure Password Hashing**
- **Account Management** with balance tracking
- **Deposit and Withdrawal** functionality
- **KYC Application Process**
- **Loan Request and Management**

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aditya-Sh77/Bank-Management-System.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd Bank-Management-System
   ```
3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python Basic Bank Management System.py
   ```
2. The application window will open. You can register a new account or log in with an existing account.

## File Structure

- **`Basic Bank Management System.py`**: The main application file containing the GUI and database logic.
- **`requirements.txt`**: List of dependencies required for the project.

## Functions

### Utility Functions

- **`hash_password(password)`**: Hashes a password for secure storage.
- **`initialize_database()`**: Initializes the SQLite database.

### GUI Application

- **`initialize_home_screen()`**: Displays the home screen with Login and Register options.
- **`show_login_screen()`**: Displays the login screen.
- **`show_register_screen()`**: Displays the registration screen.
- **`show_dashboard(account)`**: Displays the dashboard for a logged-in user.
- **`clear_screen()`**: Clears all widgets from the root window.

---

Feel free to explore the application and enhance its features!

