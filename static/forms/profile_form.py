from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import DataRequired, Length


class ProfileForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                       name='email',
                       id='email',
                       render_kw={"placeholder": "Почта"})
    name = StringField('Имя', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                       name='name',
                       id='name',
                       render_kw={"placeholder": "Имя"})
    surname = StringField('Фамилия', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                          name='surname',
                          id='surname',
                          render_kw={"placeholder": "Фамилия"})
    age = StringField('Возраст', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                      name='age',
                      id='age',
                      render_kw={"placeholder": "Возраст"})
    sex = StringField('Пол', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                      name='sex',
                      id='sex',
                      render_kw={"placeholder": "Пол"})
    hobby = StringField('Хобби', validators=[DataRequired(message='Это поле должно быть заполнено!')],
                        name='hobby',
                        id='hobby',
                        render_kw={"placeholder": "Хобби"})
