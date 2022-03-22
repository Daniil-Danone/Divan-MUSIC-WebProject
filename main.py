import os
from PIL import Image
from flask_login import LoginManager
from static.data import db_session
from static.data.users import User
from static.forms.login_form import LoginForm
from static.forms.registration_form import RegistrationForm
from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import login_user, login_required, logout_user, current_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'Divan_music'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['POST', 'GET'])
def index():
    db_session.global_init("static/databases/users.db")
    try:
        if current_user:
            image = f'/img/avatars/{current_user.email}.png'
            return render_template('index.html',
                                   title='DIVAN music',
                                   image=image)
        else:
            return render_template('index.html',
                               title='DIVAN music')
    except:
        return render_template('index.html',
                               title='DIVAN music')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    reg_form = RegistrationForm()
    user = User()
    if reg_form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == reg_form.email.data).first():
            return render_template('registration.html',
                                   title='Регистрация нового пользователя',
                                   email_exist='Пользователь с данной почтой уже существует!',
                                   form=reg_form)
        else:
            user.username = reg_form.username.data
            user.email = reg_form.email.data
            user.hashed_password = reg_form.password.data
            user.set_password(reg_form.password.data)
            if reg_form.avatar.data != '':
                try:
                    img = reg_form.avatar.data
                    filename = f'{user.email}.png'
                    img.save(filename)
                    image = Image.open(filename)
                    out_img = crop_max_square(image)
                    out_img.save(f"static/img/avatars/{user.email}.png")
                    os.remove(filename)
                except Exception as ex:
                    print(ex)
                    pass
            db_sess.add(user)
            db_sess.commit()
            return redirect('/')
    return render_template('registration.html',
                           title='Регистрация нового пользователя',
                           form=reg_form)


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == log_form.email.data).first()
        if user:
            if user.check_password(log_form.password.data):
                login_user(user, remember=log_form.remember_me.data)
                return redirect('/')
            else:
                return render_template('auth.html',
                                       form=log_form,
                                       error='Неверный пароль!')
        else:
            return render_template('auth.html',
                                   form=log_form,
                                   error='Аккаунта с таким логином не существует!')
    return render_template('auth.html',
                           form=log_form,
                           title='Авторизация - DIVAN music')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/profile')
def profile():
    return render_template('profile.html',
                           user=current_user,
                           image=f'/img/avatars/{current_user.email}.png')


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
