from flask_wtf import FlaskForm
from wtforms import EmailField
from wtforms.validators import DataRequired


class StartRegistrationForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                       name='email',
                       id='email',
                       render_kw={"placeholder": "Введите почту..."})
