import os
from PIL import Image
from datetime import datetime
from flask_login import LoginManager
from static.data import db_session
from static.data.users import User
from static.forms.registration_form import RegistrationForm
from flask import Flask, render_template, redirect, make_response, jsonify


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
    return render_template('index.html',
                           title='DIVAN MUSIC')


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
                    h, w = image.size
                    scale = 300 / max(h, w)
                    image.resize((int(h * scale), int(w * scale)),
                                 Image.ANTIALIAS).save(f"static/img/avatars/{user.email}.png")
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
