from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class StartRegistrationForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                        name='email',
                        id='email',
                        render_kw={"placeholder": "Введите почту..."})

    password = StringField('Пароль', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                 Length(min=4, max=32,
                                                        message='Длина пароля должна составлять от 4 до 32 символов!')],
                           id='password',
                           name='password',
                           render_kw={"placeholder": "Придумайте пароль..."})

    username = StringField('Ник', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                           name='username',
                           id='username',
                           render_kw={"placeholder": "Придумайте никнейм..."},)
