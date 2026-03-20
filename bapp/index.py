from flask import Flask, render_template, redirect
from flask_login import logout_user

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("/customer/home.html")

@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/register')
def register_view():
    return render_template("register.html")

@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')

@app.route('/bookings')
def bookings_view():
    return render_template("/customer/bookings.html")

if __name__ == "__main__":
    app.run(debug=True)