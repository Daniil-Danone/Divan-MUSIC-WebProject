from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField, RadioField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Ник', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                           name='username',
                           id='username',
                           render_kw={"placeholder": "Придумайте никнейм...",
                                      "autocomplete": "off"}, )

    email = StringField('Почта', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                       name='email',
                       id='email',
                       render_kw={"placeholder": "Введите почту...", "autocomplete": "off"})

    password = StringField('Пароль', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                   Length(min=4, max=32,
                                                          message='Длина пароля должна составлять от 4 до 32 символов!')],
                             id='password',
                             name='password',
                             render_kw={"placeholder": "Придумайте пароль..."})

    name = StringField('Имя',
                       id='name',
                       name='name',
                       render_kw={"placeholder": "Введите имя..."})

    surname = StringField('Фамилия',
                          id='surname',
                          name='surname',
                          render_kw={"placeholder": "Введите фамилию..."})

    age = StringField('Возраст',
                      id='age',
                      name='age',
                      render_kw={"placeholder": "Введите возраст..."})

    sex = RadioField('Пол', validators=[DataRequired('Пол не выбран!')],
                     choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')],
                     id='sex',
                     name='sex')

    hobby = StringField('Хобби, увлечения',
                        id='hobby',
                        name='hobby',
                        render_kw={"placeholder": "Перечислите свои увлечения, разделяя их запятой"})

    avatar = FileField('Аватар', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])

    accept = BooleanField('Соглашение', validators=[DataRequired()],
                          id='accept',
                          name='accept')
