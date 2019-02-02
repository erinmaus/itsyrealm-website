from flask import (
	Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for
)

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
@bp.route('/home')
def index():
	return render_template("home/index.html")
