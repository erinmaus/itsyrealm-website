from flask import (
	Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for
)

bp = Blueprint('home', __name__, url_prefix='/')

from itsyrealm.model.download import Download

@bp.route('/')
@bp.route('/home')
def index():
	latest = Download.query.order_by(Download.id.desc()).first()

	return render_template("home/index.html", latest_version=latest.version)

@bp.route('/download')
def download():
	latest = Download.query.order_by(Download.id.desc()).first()

	return render_template("home/download.html", latest_version=latest.version)