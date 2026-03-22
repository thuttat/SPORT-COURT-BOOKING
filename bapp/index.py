import cloudinary
from bapp import login_manager, db
from flask import request, redirect, render_template
from flask_login import login_user, login_required, logout_user
import cloudinary.uploader
from bapp import app, dao
from bapp.decorators import loggedin
from bapp.models import UserRole


@app.route('/login', methods=['get', 'post'])
@loggedin
def login_my_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)

            next = request.args.get('next')
            return redirect(next if next else '/')
        else:
            err_msg = 'Username hoặc password không đúng!'

    return render_template('login.html', err_msg=err_msg)

@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.route('/register', methods=['get', 'post'])
@loggedin
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            avatar_path = None
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']

            role = request.form.get('user_role')
            role_enum = UserRole.ADMIN if role == 'ADMIN' else UserRole.USER

            dao.add_user(fullname=request.form.get('fullname'),
                         username=request.form.get('username'),
                         password=password,
                         email=request.form.get('email'),
                         avatar=avatar_path,
                         user_role=role_enum)

            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)