from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class ChangePasswordForm(FlaskForm):
	current_password = PasswordField('Current Password', validators=[DataRequired()])
	new_password = PasswordField('New Password',
	validators=[
		DataRequired(),
		EqualTo('confirm_password', message='Passwords must match'),
		Length(min=24, max=255)
	])
	confirm_password = PasswordField('Confirm Password')
	submit = SubmitField()
