from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired

class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Add Book')


class IndexerForm(FlaskForm):
    name = StringField('Indexer Name', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    api_key = StringField('API Key', validators=[DataRequired()])
    submit = SubmitField('Save Indexer')


class SearchForm(FlaskForm):
    query = StringField('Search for a book', validators=[DataRequired()])
    submit = SubmitField('Search')


class DownloadClientForm(FlaskForm):
    name = StringField('Client Name', validators=[DataRequired()])
    host = StringField('Host', validators=[DataRequired()])
    port = IntegerField('Port', validators=[DataRequired()])
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Save Client')
