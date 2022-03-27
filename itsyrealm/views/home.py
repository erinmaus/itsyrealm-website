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
	latest = Release.get_latest_version(Release.TYPE_BUILD)
	if latest:
		latest_version = latest.get_version_string() 

	return render_template("home/index.html", latest_version=latest_version)

@bp.route('/play')
def play():
	return redirect(url_for('api_download.get', download_type='launcher', platform_id='Win64'))

@bp.route('/download')
def download():
	return redirect(url_for('home.play'))

@bp.route('/presskit')
def presskit():
	return render_template("home/presskit.html")
