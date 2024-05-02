# Flask Banking App

This Flask application simulates a simple banking system with features like user authentication, viewing account details, and transferring funds between accounts. It demonstrates various security vulnerabilities and how to mitigate them using Flask-WTF for CSRF protection and other security practices.

## Prerequisites

Before you can run this application, make sure you have the following installed:

- Python
- Flask
- Flask-WTF and PyJWT
- Passlib
- SQLite3

These dependencies are essential for setting up and running the Flask banking application on your local machine.

## Setup

Follow these steps to set up and run the application:

1. Clone the repository to your local machine:

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd flask-banking-app
   ```

3. Create a virtual environment:

   ```bash
   python3 -m venv env
   ```

4. Activate the virtual environment:

   ```bash
   source env/bin/activate
   ```

5. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

6. Set the Flask environment to development:

   ```bash
   export FLASK_ENV=development
   ```

7. Run the Flask application:

   ```bash
   flask run
   ```

8. Access the application in your browser at `http://localhost:5000`.

## Database Setup

To create and populate the SQLite database with sample user data, run the provided `createdb.py` script:

```bash
python bin/createdb.py
```

This script creates a `bank.db` file and inserts two user records: Alice and Bob.

## Usage

1. Open your browser and navigate to `http://localhost:5000`.
2. Use the login form to log in with the provided credentials.
3. Once logged in, you can access the dashboard, view account details, and initiate fund transfers.

## Vulnerability Demonstration

The application demonstrates various security vulnerabilities, including:

- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)

These vulnerabilities are addressed and mitigated in the application code using Flask-WTF for CSRF protection and other security best practices.

## File Structure

- `app.py`: Main Flask application code.
- `bin/createdb.py`: Script to create and populate the SQLite database.
- `bin/makeaccounts.py`: Script to create and populate the SQLite database with account data.
- `templates/`: HTML templates for rendering pages.
- `user_service.py`: Service module for user-related operations.
- `account_service.py`: Service module for account-related operations.

## Contributors

- Jaini Shah
- Krutik Doshi
- Romil Shah
- Neel Shah
