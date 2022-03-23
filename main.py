import datetime
import os
from PIL import Image
from flask_login import LoginManager
from static.data import db_session
from static.data.users import User
from static.data.posts import Post
from static.forms.post_form import PostForm
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
                                   title=f'Главная - DIVAN music',
                                   image=image,
                                   user=current_user)
        else:
            return render_template('index.html',
                                   title='Главная - DIVAN music')
    except:
        return render_template('index.html',
                               title='Главная - DIVAN music')


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
            user.name = reg_form.name.data
            user.surname = reg_form.surname.data
            user.age = int(reg_form.age.data)
            user.sex = reg_form.sex.data
            user.hobby = reg_form.hobby.data
            user.created_date = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
            user.posts = 0
            if reg_form.avatar.data != '':
                try:
                    img = reg_form.avatar.data
                    filename = f'{user.email}.png'
                    img.save(filename)
                    image = Image.open(filename)
                    out_img = crop_max_square(image)
                    out_img.save(f"static/img/avatars/{user.email}.png")
                    os.remove(filename)
                    user.avatar_path = f"/img/avatars/{user.email}.png"
                except Exception as ex:
                    print(ex)
                    pass
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
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
                           title=f'{current_user.username} - DIVAN music',
                           image=f'/img/avatars/{current_user.email}.png')


@login_required
@app.route('/add_post', methods=['POST', 'GET'])
def news():
    post_form = PostForm()
    post = Post()
    if post_form.validate_on_submit():
        db_sess = db_session.create_session()
        post.title = post_form.title.data
        post.description = post_form.description.data
        post.theme = post_form.theme.data
        post.created_date = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
        post.is_privacy = post_form.is_privacy.data
        if post_form.content.data != '':
            try:
                img = post_form.content.data
                img.save(f"static/img/post_img/{current_user.username}_{current_user.posts}.png")
                post.path = f'/img/post_img/{current_user.username}_{current_user.posts}.png'
                current_user.posts = current_user.posts + 1
                post.creator_avatar_path = current_user.avatar_path
            except Exception as ex:
                print(ex)
                pass
        post.creator = current_user.username
        db_sess.add(post)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')

    return render_template('add_post.html',
                           user=current_user,
                           title=f'Создание записи - DIVAN music',
                           image=f'/img/avatars/{current_user.email}.png',
                           form=post_form)


@app.route('/posts')
def posts():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).all()
    posts.reverse()

    nav_path = [['/', 'Главная'], ['/posts', 'Новости']]
    return render_template('posts.html',
                           user=current_user,
                           title=f'Создание записи - DIVAN music',
                           image=f'/img/avatars/{current_user.email}.png',
                           posts=posts,
                           nav_path=nav_path)


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
