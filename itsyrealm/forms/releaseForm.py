from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired
from wtforms.widgets import TextArea

from itsyrealm.model.release import Release

class ReleaseForm(FlaskForm):
	type = SelectField(
		'Release Type',
		choices=[
			(str(Release.TYPE_LAUNCHER), 'Launcher'),
			(str(Release.TYPE_BUILD), 'Build'),
			(str(Release.TYPE_RESOURCE), 'Resource')], validators=[DataRequired()])
	version_major = IntegerField('Version Major', validators=[InputRequired()])
	version_minor = IntegerField('Version Minor', validators=[InputRequired()])
	version_revision = IntegerField('Revision', validators=[InputRequired()])
	version_tag = SelectField(
		'Tag',
		choices=[
			(str(Release.TAG_ALPHA), 'Alpha'),
			(str(Release.TAG_BETA), 'Beta'),
			(str(Release.TAG_RELEASE), 'Release')], validators=[DataRequired()])
	patch_notes = StringField('Patch Notes', validators=[DataRequired()], widget=TextArea())
	submit = SubmitField()