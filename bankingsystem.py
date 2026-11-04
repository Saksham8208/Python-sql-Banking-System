import mysql.connector as M

# ------------------- CREATE DATABASE -------------------
# Connect to MySQL server (without specifying a database)
con = M.connect(
    host="localhost",
    user="root",
    password="password"
)
c = con.cursor()

# Create database (will fail if it already exists)
c.execute("CREATE DATABASE banking_db")

c.close()
con.close()

# Reconnect to the newly created database
con = M.connect(
    host="localhost",
    user="root",
    password="password",
    database="banking_db"
)
c = con.cursor()

# ------------------- ACCOUNTS TABLE -------------------
c.execute("""
CREATE TABLE accounts (
    acc_no INT PRIMARY KEY,
    name VARCHAR(100),
    balance FLOAT
)
""")

# ------------------- ACCOUNTS FUNCTIONS -------------------
def create_account():
    acc_no = int(input("Enter account number: "))
    name = input("Enter name: ")
    balance = float(input("Enter initial balance: "))
    c.execute("INSERT INTO accounts (acc_no, name, balance) VALUES (%s, %s, %s)", (acc_no, name, balance))
    con.commit()
    print("Account created successfully!\n")

def view_accounts():
    c.execute("SELECT * FROM accounts")
    rows = c.fetchall()
    if rows:
        print("Account Number   Name             Balance")
        print("----------------------------------------")
        for r in rows:
            print(f"{r[0]}   {r[1]}   Rs.{r[2]:.2f}")
    else:
        print("No accounts found.")

# ------------------- TRANSACTIONS TABLE -------------------
c.execute("""
CREATE TABLE transactions (
    txn_id INT PRIMARY KEY,
    acc_no INT,
    txn_type VARCHAR(10),
    amount FLOAT,
    txn_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (acc_no) REFERENCES accounts(acc_no)
)
""")

# ------------------- TRANSACTIONS FUNCTIONS -------------------
def create_transaction():
    txn_id = int(input("Enter transaction ID: "))
    acc_no = int(input("Enter account number: "))
    txn_type = input("Enter transaction type (deposit/withdraw): ").lower()
    amount = float(input("Enter amount: "))

    c.execute("SELECT balance FROM accounts WHERE acc_no=%s", (acc_no,))
    bal = c.fetchone()

    if txn_type == "deposit":
        if bal is not None:
            c.execute("UPDATE accounts SET balance = balance + %s WHERE acc_no = %s", (amount, acc_no))
        else:
            print("Account does not exist.")
            return
    elif txn_type == "withdraw":
        if bal is not None and bal[0] >= amount:
            c.execute("UPDATE accounts SET balance = balance - %s WHERE acc_no = %s", (amount, acc_no))
        else:
            print("Not enough balance or account does not exist.")
            return

    c.execute(
        "INSERT INTO transactions (txn_id, acc_no, txn_type, amount) VALUES (%s, %s, %s, %s)",
        (txn_id, acc_no, txn_type, amount)
    )
    con.commit()
    print("Transaction completed successfully!\n")

def view_transactions():
    c.execute("SELECT * FROM transactions")
    rows = c.fetchall()
    if rows:
        print("Transaction ID   Account No   Type      Amount   Date")
        print("---------------------------------------------------")
        for r in rows:
            print(f"{r[0]}   {r[1]}   {r[2]}   Rs.{r[3]}   {r[4]}")
    else:
        print("No transactions found.")

# ------------------- BRANCHES TABLE -------------------
c.execute("""
CREATE TABLE branches (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(100),
    branch_city VARCHAR(100)
)
""")

# ------------------- BRANCHES FUNCTIONS -------------------
def create_branch():
    branch_id = int(input("Enter branch ID: "))
    branch_name = input("Enter branch name: ")
    branch_city = input("Enter branch city: ")
    c.execute("INSERT INTO branches (branch_id, branch_name, branch_city) VALUES (%s, %s, %s)", (branch_id, branch_name, branch_city))
    con.commit()
    print("Branch created successfully!\n")

def view_branches():
    c.execute("SELECT * FROM branches")
    rows = c.fetchall()
    if rows:
        print("Branch ID   Branch Name      City")
        print("-----------------------------------")
        for r in rows:
            print(f"{r[0]}   {r[1]}   {r[2]}")
    else:
        print("No branches found.")

# ------------------- MAIN MENU -------------------
while True:
    print("\nMenu:")
    print("1. Create Account")
    print("2. View Accounts")
    print("3. Create Transaction")
    print("4. View Transactions")
    print("5. Create Branch")
    print("6. View Branches")
    print("7. Exit")

    ch = input("Enter choice: ")

    if ch == "1":
        create_account()
    elif ch == "2":
        view_accounts()
    elif ch == "3":
        create_transaction()
    elif ch == "4":
        view_transactions()
    elif ch == "5":
        create_branch()
    elif ch == "6":
        view_branches()
    elif ch == "7":
        break
    else:
        print("Invalid choice.")

c.close()
con.close()
