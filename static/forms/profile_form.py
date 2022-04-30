from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class ProfileForm(FlaskForm):
    email = EmailField('Почта', name='email', id='email', render_kw={"placeholder": "Почта", "disabled": True})

    name = StringField('Имя', name='name', id='name', render_kw={"placeholder": "Имя"})

    surname = StringField('Фамилия', name='surname', id='surname', render_kw={"placeholder": "Фамилия"})

    age = StringField('Возраст', name='age', id='age', render_kw={"placeholder": "Возраст"})

    sex = StringField('Пол', name='sex', id='sex', render_kw={"placeholder": "Пол"})

    hobby = StringField('Хобби', name='hobby', id='hobby', render_kw={"placeholder": "Хобби"})

    avatar = FileField('Контент', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])

    submit_btn = SubmitField('Сохранить изменения', id='profile__save')
