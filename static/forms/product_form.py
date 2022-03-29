from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, StringField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed


class ProductForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                Length(min=3, max=100)],
                        name='title',
                        id='title',
                        render_kw={"placeholder": "Название товара..."})

    description = TextAreaField('Описание', validators=[Length(max=10000)],
                                id='description',
                                name='description',
                                render_kw={"placeholder": "Описание товара"})

    theme = SelectField('Категория товара',
                        choices=[(None, 'Выберите категорию товара'),
                                 ('Ноты', 'Ноты'),
                                 ('Услуги', 'Услуги')]
                        )

    content = FileField('Вложения', validators=[FileAllowed(['pdf', 'gp', 'gpx', 'gp5', 'doc', 'docx', 'txt'])])

    price = FloatField('Цена (от 1$ до 999$)', validators=[DataRequired(message='Это поле должно быть заполнено!'),
                                                           NumberRange(min=1, max=999)],
                       name='price',
                       id='price',
                       render_kw={"placeholder": "Цена товара..."}
                       )
