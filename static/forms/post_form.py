from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, StringField, BooleanField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                 Length(min=3, max=100)],
                        name='title',
                        id='title',
                        render_kw={"placeholder": "Придумайте заголовок записи..."})

    description = TextAreaField('Описание', validators=[Length(max=10000)],
                                id='description',
                                name='description',
                                render_kw={"placeholder": "Придумайте описание для своей записи..."})

    theme = SelectField('Тематика',
                        choices=[('Творчество', 'Творчество'), ('Юмор', 'Юмор'), ('Обсуждения', 'Обсуждения')])

    content = FileField('Контент', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])

    is_privacy = BooleanField('Скрыть?', name='is_privacy', id='is_privacy')
