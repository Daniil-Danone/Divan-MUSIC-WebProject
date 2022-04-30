import os
import random
import fitz
import yadisk
import datetime
import requests
import asyncio
from PIL import Image
from flask_login import LoginManager
from static.data import db_session
from static.data.users import User
from static.data.posts import Post
from static.data.products import Product
from static.forms.post_form import PostForm
from static.forms.login_form import LoginForm
from static.forms.product_form import ProductForm
from static.forms.start_registration import RegistrationForm
from static.forms.profile_form import ProfileForm

from flask import Flask, render_template, redirect, make_response, jsonify, request, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'Divan_music'

yandex_disk_token = os.environ.get('YANDEX_DISK_API')
disk = yadisk.YaDisk(token=yandex_disk_token)


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
    if current_user.is_authenticated:
        avatar = f'/img/avatars/{current_user.email}.png'
        return render_template('index.html',
                               title=f'Главная - DIVAN music',
                               image=avatar,
                               user=current_user)
    else:
        log_form = LoginForm()
        if log_form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == log_form.email.data).first()
            if user:
                if user.check_password(log_form.password.data):
                    login_user(user, remember=log_form.remember_me.data)
                    return redirect('/')
                else:
                    return render_template('index.html',
                                           form=log_form,
                                           error='Неверный пароль!',
                                           title='Авторизация - DIVAN music')
            else:
                return render_template('index.html',
                                       form=log_form,
                                       error='Аккаунта с таким логином не существует!',
                                       title='Авторизация - DIVAN music')
        return render_template('index.html',
                               form=log_form,
                               title='Главная - DIVAN music')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    user = User()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html',
                                   title='Регистрация',
                                   form=form,
                                   email_error='Почта занята!')
        else:
            print("Проверка саксес")
            user.email = form.email.data
            user.username = form.username.data
            user.set_password(form.password.data)
            user.username = form.username.data
            user.created_date = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')

            user.posts = 0
            user.name = ''
            user.surname = ''
            user.sex = ''
            user.age = ''
            user.hobby = ''

            db_sess.add(user)
            db_sess.commit()
            login_user(user)
        return redirect('/')

    return render_template('registration.html',
                           title='Регистрация',
                           form=form)


# def registration():
#     db_sess = db_session.create_session()
#     form = RegistrationForm()
#     user = User()
#     if form.validate_on_submit():
#         if db_sess.query(User).filter(User.email == form.email.data).first():
#             return render_template('registration_template.html',
#                                    title='Регистрация',
#                                    form=form,
#                                    message="Пользователь с данной почтой уже зарегистрирован в системе")
#         else:
#             user.username = form.username.data
#             user.email = form.email.data
#             user.hashed_password = form.password.data
#             user.set_password(form.password.data)
#             user.name = form.name.data
#             user.surname = form.surname.data
#             user.sex = form.sex.data
#             user.age = str(form.age.data)
#             user.hobby = form.hobby.data
#             user.created_date = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
#             if form.avatar.data != '':
#                 img = form.avatar.data
#                 filename = f'{form.email.data}.png'
#                 img.save(filename)
#                 image = Image.open(filename)
#                 out_img = crop_max_square(image)
#                 out_img.save(f"static/img/avatars/{form.email.data}.png")
#                 user.avatar_path = f"/img/avatars/{form.email.data}.png"
#                 os.remove(filename)
#             db_sess.add(user)
#             db_sess.commit()
#             login_user(user)
#             return redirect('/')
#     return render_template('registration_template.html',
#                            title='Регистрация',
#                            form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = ProfileForm()

    if request.method == 'GET':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        if user:
            form.email.data = user.email
            form.name.data = user.name
            form.surname.data = user.surname
            form.age.data = user.age
            form.sex.data = user.sex
            form.hobby.data = user.hobby
        else:
            abort(404)

    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            user.name = form.name.data
            user.surname = form.surname.data
            user.age = form.age.data
            user.sex = form.sex.data
            user.hobby = form.hobby.data

            if form.avatar.data is not None:
                img = form.avatar.data
                filename = f'{form.email.data}.png'
                img.save(filename)
                image = Image.open(filename)
                out_img = crop_max_square(image)
                out_img.save(f"static/img/avatars/{form.email.data}.png")
                user.avatar_path = f"/img/avatars/{form.email.data}.png"
                try:
                    os.replace(filename, 'static/img/avatars')
                except:
                    pass
            db_sess.commit()
            return redirect('/profile')
        else:
            abort(404)

    return render_template('profile.html',
                           user=current_user,
                           form=form,
                           title=f'{current_user.username} - DIVAN music',
                           image=f'/img/avatars/{current_user.email}.png')


@login_required
@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    db_sess = db_session.create_session()
    post_form = PostForm()
    post = Post()
    user = db_sess.query(User).filter(User.email == current_user.email).first()
    if post_form.validate_on_submit():
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
                user.posts = user.posts + 1
            except Exception as ex:
                print(ex)
                pass
        post.creator_avatar_path = current_user.avatar_path
        post.creator = current_user.username
        db_sess.add(post)
        db_sess.commit()
        return redirect('/posts')

    return render_template('add_post.html',
                           user=current_user,
                           title=f'Создание записи - DIVAN music',
                           image=f'/img/avatars/{current_user.email}.png',
                           form=post_form)


@app.route('/posts')
def posts():
    db_sess = db_session.create_session()
    posts_list = db_sess.query(Post).all()
    posts_list.reverse()

    nav_path = [['/', 'Главная'], ['/posts', 'Новости']]

    if len(posts_list) == 0:
        is_there_posts = True
    else:
        is_there_posts = None

    if current_user.is_authenticated:
        image = current_user.email
        log_form = None
    else:
        image = None
        log_form = LoginForm()

    return render_template('posts.html',
                           user=current_user,
                           title=f'Создание записи - DIVAN music',
                           image=f'/img/avatars/{image}.png',
                           posts=posts_list,
                           nav_path=nav_path,
                           form=log_form,
                           is_there_posts=is_there_posts)


@app.route('/posts/delete/<int:post_id>')
def post_delete(post_id):
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == post_id).first()
    if post:
        db_sess.delete(post)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/posts')


@app.route('/marketplace')
def marketplace():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    products.reverse()
    if current_user.is_authenticated:
        image = current_user.email
        log_form = None

    else:
        image = None
        log_form = LoginForm()
    return render_template('marketplace_main_page.html',
                           user=current_user,
                           title=f'Маркетплейс - DIVAN music',
                           image=f'/img/avatars/{image}.png',
                           products=products,
                           form=log_form)


@app.route('/marketplace/product_id_<int:product_id>')
def product_page(product_id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).get(product_id)
    disk.publish(product.path)
    download_link = disk.get_download_link(product.path)
    print(download_link)
    if current_user.is_authenticated:
        image = current_user.email
        log_form = None

    else:
        image = None
        log_form = LoginForm()
    return render_template('product__page.html',
                           user=current_user,
                           title=f'{product.title} - DIVAN music',
                           image=f'/img/avatars/{image}.png',
                           product=product,
                           download=download_link,
                           form=log_form)


@app.route('/marketplace/downloading/product_id_<int:product_id>')
def download_file(product_id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).get(product_id)
    disk.publish(product.path)
    download_request = requests.get(disk.get_download_link(product.path))
    with open(rf'C:\Downloads\{product.content}', 'wb') as f:
        f.write(download_request.content)
    return redirect(f'/marketplace/product_id_{product_id}')


@login_required
@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    product_form = ProductForm()
    product = Product()
    error = None

    if product_form.validate_on_submit():
        db_sess = db_session.create_session()
        product.title = product_form.title.data
        product.description = product_form.description.data
        product.theme = product_form.theme.data
        product.price = product_form.price.data

        if product_form.content.data:
            file = product_form.content.data
            filename = secure_filename(product_form.content.data.filename)
            file.save(f'static/products/documents/{filename}')
            filepath = f'static/products/documents/{filename}'
            product.local_path = f'/static/products/documents/{filename}'
            if filename.split('.')[-1] == 'pdf':
                product.icon_file = '/img/icons/pdf3.png'
                zoom_x = 2.0
                zoom_y = 2.0
                mat = fitz.Matrix(zoom_x, zoom_y)
                try:
                    doc = fitz.open(filepath)
                    for page in doc:
                        pix = page.get_pixmap(matrix=mat)
                        pix.save(f"static/img/products/preview/{filename.replace('.pdf', '')}_preview.png")
                        break
                except Exception as ex:
                    print(ex)

                img = Image.open(f"static/img/products/preview/{filename.replace('.pdf', '')}_preview.png")
                watermark = Image.open('static/img/products/preview/Watermark.png')
                img.paste(watermark, (0, 0), watermark)
                img.save(f"static/img/products/preview/{filename.replace('.pdf', '')}_preview.png")
                product.preview_path = f"/img/products/preview/{filename.replace('.pdf', '')}_preview.png"

            elif filename.split('.')[-1] == 'txt':
                product.icon_file = '/img/icons/txt.png'
            elif filename.split('.')[-1] == 'doc' or filename.split()[-1] == 'docx':
                product.icon_file = '/img/icons/doc.png'
            elif filename.split('.')[-1] == 'gp' or filename.split()[-1] == 'gpx' or filename.split()[-1] == 'gp5':
                product.icon_file = '/img/icons/gpx.png'
            else:
                product.icon_file = None

            if not disk.exists(f"/Site-products/{current_user.email}"):
                disk.mkdir(f"/Site-products/{current_user.email}")
            if not disk.exists(f"/Site-products/{current_user.email}/{filename}"):
                disk.upload(filepath, f"/Site-products/{current_user.email}/{filename}")
                product.path = f"/Site-products/{current_user.email}/{filename}"
                product.content = filename
            else:
                while True:
                    new_filename = filename.replace(filename.split('.')[-1], '').rstrip('.') + \
                                   str(random.randrange(0, 9999)) + '.' + filename.split('.')[-1]
                    if not disk.exists(f"/Site-products/{current_user.email}/{new_filename}"):
                        break
                disk.upload(filepath, f"/Site-products/{current_user.email}/{new_filename}")
                product.path = f"/Site-products/{current_user.email}/{new_filename}"
                product.content = new_filename

        else:
            error = 'Вы должны добавить продукт (ноты)'

        product.creator = current_user.username
        product.creator_avatar_path = current_user.avatar_path
        product.is_sold = False
        product.created_date = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')

        if error:
            product_form.title.data = product.title
            product_form.description.data = product.description
            product_form.theme.data = product.theme
            product_form.price.data = product.price
            product_form.content.data = product.content
            return render_template('add_product.html',
                                   user=current_user,
                                   title=f'Создание записи - DIVAN music',
                                   image=f'/img/avatars/{current_user.email}.png',
                                   error=error,
                                   form=product_form)
        else:
            db_sess.add(product)
            db_sess.merge(current_user)
            db_sess.commit()

            return redirect('/marketplace')

    return render_template('add_product.html',
                           user=current_user,
                           title=f'Создание записи - DIVAN music',
                           image=f'/img/avatars/{current_user.email}.png',
                           form=product_form)


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def delete_image(path):
    os.remove(path)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
