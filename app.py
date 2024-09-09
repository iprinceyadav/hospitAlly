from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.hospital_management

# Home route
@app.route('/')
def home():
    return render_template('login.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form['user_type']
        email = request.form['email']
        password = request.form['password']
        
        # User verification logic
        user = db[user_type].find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['email'] = email
            session['user_type'] = user_type
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'

    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_type = request.form['user_type']
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        # Store the user in the respective collection based on user_type
        db[user_type].insert_one({'name': name, 'email': email, 'password': password})
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return render_template('dashboard.html', user_type=session['user_type'])
    else:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
