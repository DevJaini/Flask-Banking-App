import sqlite3
from passlib.hash import pbkdf2_sha256

def setup_database():
    try:
        # Connect to the SQLite database
        con = sqlite3.connect('bank.db')
        cur = con.cursor()

        # Creating the 'users' table
        cur.execute('''
            CREATE TABLE users (
                email TEXT PRIMARY KEY,
                name TEXT,
                password TEXT)
        ''')

        # Inserting user data
        users_data = [
            ('alice@example.com', 'Alice Xu', pbkdf2_sha256.hash("123456")),
            ('bob@example.com', 'Bobby Tables', pbkdf2_sha256.hash("123456"))
        ]
        for user in users_data:
            cur.execute("INSERT INTO users VALUES (?, ?, ?)", user)
            
        # Commit the changes 
        con.commit()
    except sqlite3.IntegrityError as e:
        # Handle database integrity errors, such as violating primary key constraints.
        print(f"Database error related to data integrity: {e}")
    except sqlite3.OperationalError as e:
        # Handle operational errors related to SQLite database operations.
        print(f"Operational error related to SQLite database operations: {e}")
    except Exception as e:
        # Handle unexpected errors.
        print(f"An unexpected error occurred: {e}")
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    # Call the setup_database function to create and populate the 'users' table.
    setup_database()
