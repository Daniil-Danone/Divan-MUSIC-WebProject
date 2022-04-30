from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, BooleanField, StringField, RadioField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                       name='email',
                       id='email',
                       render_kw={"placeholder": "Введите логин (почту)..."})

    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                   Length(min=4, max=32,
                                                          message='Длина пароля должна составлять от 4 до 32 символов!')],
                             id='password',
                             name='password',
                             render_kw={"placeholder": "Введите пароль..."})

    remember_me = BooleanField('Запомнить меня',
                               id='custom__checkbox')

