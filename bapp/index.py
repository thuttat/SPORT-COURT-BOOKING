import datetime
from flask import Flask, render_template, redirect
from flask_login import logout_user

app = Flask(__name__)

@app.route('/')
def index():
    courts = [
        {
            "id": "c1",
            "name": "Sân bóng đá Mini A",
            "sport": "football",
            "location": "Quận 1",
            "price": 200000,
            "rating": 4.5,
            "available": True
        },
        {
            "id": "c2",
            "name": "Sân cầu lông VIP 1",
            "sport": "badminton",
            "location": "Quận 3",
            "price": 80000,
            "rating": 4.8,
            "available": True
        },
        {
            "id": "c3",
            "name": "Sân cầu lông TTTM",
            "sport": "badminton",
            "location": "Quận 8",
            "price": 45000,
            "rating": 4.9,
            "available": False
        },
        {
            "id": "c4",
            "name": "Sân tennis trung tâm",
            "sport": "tennis",
            "location": "Quận 7",
            "price": 300000,
            "rating": 4.6,
            "available": True
        },
        {
            "id": "c5",
            "name": "Sân tennis Hồ Tùng Mậu",
            "sport": "tennis",
            "location": "Quận 1",
            "price": 500000,
            "rating": 4.7,
            "available": True
        }
    ]
    return render_template("customer/home.html", courts=courts, current_date=datetime.date.today().strftime("%Y-%m-%d"))

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
    return render_template("customer/bookings.html")

@app.route('/profile')
def profile_view():
    return render_template("customer/profile.html")

if __name__ == "__main__":
    app.run(debug=True)