import os
import hashlib

from flask import (
	Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for
)
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from itsyrealm.common.auth import login as login_user, logout as logout_user
from itsyrealm.common.database import get_database
from itsyrealm.forms.loginForm import LoginForm
from itsyrealm.forms.changePasswordForm import ChangePasswordForm
from itsyrealm.model.user import User

bp = Blueprint('admin_home', __name__, url_prefix='/admin')

@bp.route('/')
@login_required
def index():
	return render_template("admin/home/index.html", user=current_user)

@bp.route('/logout')
@login_required
def logout():
	logout_user()

	flash("You have been logged out.")

	return redirect(url_for("admin_home.login"))

@bp.route('/password', methods=('GET', 'POST'))
@login_required
def password():
	form = ChangePasswordForm()

	if form.validate_on_submit():
		user = current_user.get_user()
		if user and check_password_hash(user.password_hash, form.current_password.data):
			user.password_hash = generate_password_hash(form.new_password.data)
			db = get_database()
			db.session.add(user)
			db.session.commit()

			flash("You password was updated.")
		else:
			flash("Current password wrong.")

	return render_template("admin/home/password.html", form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and check_password_hash(user.password_hash, form.password.data):
			login_user(user)
			return redirect(url_for("admin_home.index"))

		flash("Invalid username and/or password.")

	return render_template("admin/home/login.html", form=form)
