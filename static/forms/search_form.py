from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    search__field = StringField('Поиск', id="search__field")
    submit = SubmitField('')
