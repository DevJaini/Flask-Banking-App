import sqlite3

# Function to retrieve the balance of an account
def get_balance(account_number, owner):
    con = None
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        # Retrieve balance for the specified account and owner
        cur.execute('SELECT balance FROM accounts WHERE id=? AND owner=?', (account_number, owner))
        row = cur.fetchone()
        if row is None:
            return None
        return row[0]  # Return the balance
    except sqlite3.Error as e:
        print("Error:", e)
        return None
    finally:
        if con:
            con.close()  # Close the database connection

# Function to perform a fund transfer between accounts
def do_transfer(source, target, amount):
    con = None
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        # Check if the target account exists
        cur.execute('SELECT id FROM accounts WHERE id=?', (target,))
        row = cur.fetchone()
        if row is None:
            return False  # Return False if the target account doesn't exist
        
        con.execute('BEGIN')  # Start transaction
        
        # Deduct the specified amount from the source account
        cur.execute('UPDATE accounts SET balance=balance-? WHERE id=? AND balance>=?', (amount, source, amount))
        if cur.rowcount == 0:
            con.rollback()  # Rollback if source account doesn't have enough funds
            return False  # Return False to indicate insufficient funds
        
        # Add the transferred amount to the target account
        cur.execute('UPDATE accounts SET balance=balance+? WHERE id=?', (amount, target))
        
        con.commit()  # Commit transaction
        return True  # Return True to indicate successful transfer
    except sqlite3.Error as e:
        print("Error:", e)
        return False  # Return False to indicate failure
    finally:
        if con:
            con.close()  # Close the database connection
