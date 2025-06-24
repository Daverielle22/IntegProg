from flask import Flask, request, redirect, render_template_string
import hashlib
import os
import json

app = Flask(__name__)
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    return redirect("/index.html")

@app.route('/register', methods=['POST'])
def register():
    users = load_users()
    username = request.form['username']
    password = request.form['password']
    if username in users:
        return "Username already exists. Try another."
    users[username] = hash_password(password)
    save_users(users)
    return "Registered successfully. <a href='/index.html'>Login</a>"

@app.route('/login', methods=['POST'])
def login():
    users = load_users()
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == hash_password(password):
        return f"Welcome, {username}!"
    return "Invalid credentials. <a href='/index.html'>Try again</a>"

@app.route('/<path:filename>')
def serve_static(filename):
    return open(filename).read()

if __name__ == "__main__":
    app.run(debug=True)
