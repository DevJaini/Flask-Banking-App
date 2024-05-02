import sqlite3
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from flask import Flask, request, g
from flask_wtf import CSRFProtect
import jwt
import secrets

# Initialize Flask app
app = Flask(__name__)

# Set up CSRF protection
csrf = CSRFProtect(app)

# Generate a secure secret key
SECRET_KEY = secrets.token_urlsafe(16)
app.config['SECRET_KEY'] = SECRET_KEY

# Configure cookie security
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

def get_user_with_credentials(email, password):
    try:
        # Connect to the database
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        
        # Retrieve user data from the database based on email
        cursor.execute('SELECT email, name, password FROM users WHERE email=?', (email,))
        user_data = cursor.fetchone()
        
        # Close the database connection
        conn.close()
        
        # Check if user exists and password is correct
        if user_data is not None and pbkdf2_sha256.verify(password, user_data[2]):
            # If credentials are valid, return user information with a generated token
            return {"email": user_data[0], "name": user_data[1], "token": generate_token(user_data[0])}
        else:
            return None
    except Exception as e:
        # Error handling for database connection or query issues
        return {"error": str(e), "status": 500}

def logged_in():
    # Check if the user is logged in by verifying the authenticity of the JWT token
    token = request.cookies.get('auth_token')
    try:
        # Decode the JWT token and extract user information
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        g.user = data['sub']  # Store the user's email in Flask global object 'g'
        return True
    except jwt.InvalidTokenError:
        return False

def generate_token(email):
    try:
        # Generate a JWT token with user email as subject ('sub')
        now = datetime.utcnow()
        payload = {'sub': email, 'iat': now, 'exp': now + timedelta(minutes=60)}  # Token expires in 60 minutes
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return {"error": str(e), "status": 500}
