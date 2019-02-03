from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

from itsyrealm.model.download import Download

class DownloadForm(FlaskForm):
	binary = FileField('Binary')
	type = SelectField(
		'Binary Type',
		choices=[
			(str(Download.TYPE_LAUNCHER), 'Launcher'),
			(str(Download.TYPE_BUILD), 'Build'),
			(str(Download.TYPE_RESOURCE), 'Resource')], validators=[DataRequired()])
	platform = SelectField(
		'Platform',
		choices=[
			('Win32', 'Win32'),
			('Win64', 'Win64'),
			('Linux32', 'Linux32'),
			('Linux64', 'Linux64'),
			('macOS', 'macOS')
		], validators=[DataRequired()])
	version = StringField('Version', validators=[DataRequired()])
	patch_notes = StringField('Patch Notes', validators=[DataRequired()], widget=TextArea())
	submit = SubmitField()