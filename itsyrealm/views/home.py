from flask import (
	Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for
)

bp = Blueprint('home', __name__, url_prefix='/')

from itsyrealm.model.release import Release

@bp.route('/')
@bp.route('/home')
def index():
	latest_version = ""
	latest = Release.get_latest_version()
	if latest:
		latest_version = latest.get_version_string() 

	return render_template("home/index.html", latest_version=latest_version)

@bp.route('/download')
def download():
	latest_version = ""
	latest = Release.get_latest_version()
	if latest:
		latest_version = latest.get_version_string() 

	return render_template("home/download.html", latest_version=latest_version)