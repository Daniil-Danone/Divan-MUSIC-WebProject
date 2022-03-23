from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField, RadioField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Ник', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                           name='username',
                           id='username',
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

    name = StringField('Имя', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                       id='name',
                       name='name',
                       render_kw={"placeholder": "Введите имя..."})

    surname = StringField('Фамилия', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                          id='surname',
                          name='surname',
                          render_kw={"placeholder": "Введите фамилию..."})

    age = StringField('Возраст', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                      id='age',
                      name='age',
                      render_kw={"placeholder": "Введите возраст..."})

    sex = RadioField('Пол', validators=[DataRequired('Пол не выбран!')],
                     choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')],
                     id='sex',
                     name='sex')

    hobby = StringField('Хобби, увлечения', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                        id='hobby',
                        name='hobby',
                        render_kw={"placeholder": "Перечислите свои увлечения, разделяя их запятой"})

    avatar = FileField('Аватар', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])

    accept = BooleanField('Соглашение', validators=[DataRequired()],
                          id='accept',
                          name='accept')
