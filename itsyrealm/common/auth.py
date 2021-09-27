from flask_login import (
	LoginManager, login_user, logout_user, current_user,
	login_required
)

from itsyrealm.model.user import User

login_manager = LoginManager()

class LoggedInUser:
	def __init__(self, user):
		self._user = user
		if user:
			self.is_authenticated = True
			self.is_active = True
			self.is_anonymous = False

	def get_user(self):
		return self._user

	def get_id(self):
		if self._user:
			return str(self._user.id)
		else:
			return "0"

def init_app(app):
	login_manager.init_app(app)
	login_manager.login_view = "admin_home.login"

	@login_manager.user_loader
	def load_user(user_id):
		user = User.query.filter_by(id=int(user_id)).first()
		return LoggedInUser(user)

def login(user):
	login_user(LoggedInUser(user))

def logout():
	logout_user()
