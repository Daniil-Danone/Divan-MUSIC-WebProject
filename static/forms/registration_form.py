from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField, RadioField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Ник', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                           name='surname',
                           id='surname',
                           render_kw={"placeholder": "Придумайте никнейм..."}, )

    email = EmailField('Почта', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                       name='email',
                       id='email',
                       render_kw={"placeholder": "Введите почту..."})

    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                   Length(min=4, max=32,
                                                          message='Длина пароля должна составлять от 4 до 32 символов!')],
                             id='password',
                             name='password',
                             render_kw={"placeholder": "Придумайте пароль..."})

    avatar = FileField('Аватар', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])

    accept = BooleanField('Соглашение', validators=[DataRequired()],
                          id='accept',
                          name='accept')
