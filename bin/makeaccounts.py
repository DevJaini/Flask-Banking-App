import sqlite3

def create_accounts():
    try:
        # Connect to the SQLite database
        con = sqlite3.connect('bank.db')
        cur = con.cursor()

        # Create the accounts table if it does not exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id TEXT PRIMARY KEY,
                owner TEXT,
                balance INTEGER,
                FOREIGN KEY(owner) REFERENCES users(email)
            )''')

        # Insert initial data into accounts table
        accounts_data = [
            ('100', 'alice@example.com', 7500),
            ('190', 'alice@example.com', 200),
            ('998', 'bob@example.com', 1000)
        ]
        cur.executemany("INSERT INTO accounts VALUES (?, ?, ?)", accounts_data)

        # Commit the transaction
        con.commit()  
        print("Accounts table created and initial data inserted successfully.")
    except sqlite3.Error as e:
        # Handle SQLite errors
        print(f"Database error: {e}")  
    except Exception as e:
        # Handle general errors
        print(f"An unexpected error occurred: {e}")  
    finally:
        if con:
            con.close()  # Close the database connection

if __name__ == "__main__":
    create_accounts()
