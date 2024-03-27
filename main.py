from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

def load_data(category):
    data_folder = 'data'
    filename = os.path.join(data_folder, f'{category}.json')
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

@app.route("/")
def index():
    category = request.args.get('category', 'all')
    if category == 'all':
        data = load_data('tech') + load_data('romance') + load_data('horror') + load_data('psychology')
    elif category in ['tech', 'romance', 'horror', 'psychology']:
        data = load_data(category)
    else:
        data = []
    return render_template('index.html', data=data, category=category)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password before saving to the database
        hashed_password = generate_password_hash(password)

        # Create a new user instance
        new_user = User(username=username, email=email, password=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        # Check if the username or email exists in the database
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and check_password_hash(user.password, password):
            # Store the user's ID in the session
            session['user_id'] = user.id
            return redirect('/account')
        else:
            error = 'Invalid username/email or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/account')
def account():
    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('account.html', user=user)
    else:
        return redirect('/login')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    if query:
        with open('data.json') as f:
            data = json.load(f)
        search_results = [item for item in data if query.lower() in item['name'].lower()]
        return render_template('search.html', query=query, results=search_results)
    else:
        return render_template('search.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_message="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500


if __name__ == "__main__":
    app.run(debug=True)
