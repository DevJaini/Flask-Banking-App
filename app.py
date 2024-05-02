from flask import Flask, request, make_response, redirect, render_template, g, abort
from user_service import get_user_with_credentials, logged_in
from account_service import get_balance, do_transfer
from flask_wtf.csrf import CSRFProtect, generate_csrf
import secrets
import time

app = Flask(__name__)
# Generating a secret key using a cryptographically secure method for Flask app's security.
secret_key = secrets.token_urlsafe(16) 
app.config['SECRET_KEY'] = secret_key
# Initializing CSRF protection for the Flask app.
csrf = CSRFProtect(app)  

@app.route("/", methods=['GET'])
def home():
    if not logged_in():
        # Render the login page if the user is not logged in.
        return render_template("login.html")
    # Redirect to the dashboard if the user is already logged in.
    return redirect('/dashboard')

@app.route("/login", methods=["POST"])
def login():
    # Retrieve email and password from the form submission.
    email = request.form.get("email")
    password = request.form.get("password")
    # Authenticate the user with provided credentials.
    user = get_user_with_credentials(email, password)

    # Introducing a delay to mitigate timing attacks which can be exploited for user enumeration.
    time.sleep(1)

    if not user:
        # Render the login page with an error message for invalid credentials.
        return render_template("login.html", error="Invalid credentials")
    
    response = make_response(redirect("/dashboard"))
    # Setting secure cookies to prevent XSS attacks and ensuring cookies are transmitted over HTTPS only.
    response.set_cookie("auth_token", user["token"], httponly=True, secure=True)
    return response, 303

@app.route("/dashboard", methods=['GET'])
def dashboard():
    if not logged_in():
        # Redirect to the login page if the user is not logged in.
        return redirect('/login')
    # Render the dashboard template with the user's email.
    return render_template("dashboard.html", email=g.user)

@app.route("/details", methods=['GET'])
def details():
    if not logged_in():
        # Redirect to the login page if the user is not logged in.
        return redirect('/login')
    # Retrieve account details and balance.
    account_number = request.args.get('account')
    balance = get_balance(account_number,  g.user)
    return render_template("details.html", user= g.user, account_number=account_number, balance=balance)

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if not logged_in():
        # Redirect to the login page if the user is not logged in.
        return redirect('/login')

    if request.method == "POST":
        # Retrieve transfer details from the form submission.
        source = request.form.get("from")
        to_email = request.form.get("to_email")  
        to_account = request.form.get("to_account") 
        amount = request.form.get("amount")

        # Validating that all required fields are provided.
        if not source or not to_email or not to_account or not amount:
            abort(400, "All fields are required for the transfer")

        try:
            amount = int(amount)  # Convert amount to integer.
        except ValueError:
            abort(400, "Invalid amount format")

        if amount < 0:
            abort(400, "Amount cannot be negative") 

        if amount > 1000:
            abort(400, "Transfer amount exceeds maximum limit")

        # Retrieve balances of source and target accounts.
        source_balance = get_balance(source, g.user)
        target_balance = get_balance(to_account, to_email)

        if source_balance is None or target_balance is None:
            abort(404, "Source or target account not found")  

        if amount > source_balance:
            abort(400, "Insufficient balance for transfer") 

        # Perform the fund transfer.
        success = do_transfer(source, to_account, amount)

        if success:
            # Render the dashboard with a success message if transfer is successful.
            message = f"Transfer of {amount} from account {source} to account {to_account} was successful."
            return render_template("dashboard.html", message=message, email=g.user)
        else:
            abort(500, "Internal Server Error")

    return render_template("transfer.html")

@app.route("/logout", methods=['GET'])
def logout(): 
    response = make_response(redirect("/"))
    # Securely logging out by deleting the authentication token.
    response.delete_cookie('auth_token')  
    return response, 303

@app.before_request
def before_request():
    # Generating a CSRF token for each request to mitigate CSRF attacks.
    g.csrf_token = generate_csrf()

if __name__ == "__main__":
    app.run(debug=True)
