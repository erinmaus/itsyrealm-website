from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField

class PhotoForm(FlaskForm):
	thumb = FileField('thumb', description='Thumbnail')
	full = FileField('full', description='Full-Sized Image')
	title = StringField('title', description='Title')
	description = StringField('description', description='Description')
