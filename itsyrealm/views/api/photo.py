import os

from flask import (
	Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for, jsonify, send_file, abort
)

bp = Blueprint('api_photo', __name__, url_prefix='/api/photo')

from itsyrealm.model.photo import Photo

@bp.route('/list')
def index():
	photos = Photo.query.all()
	photos = [photo.serialize() for photo in photos]
	return jsonify(photos)

@bp.route('/view/full/<int:photo_id>')
def view_full(photo_id):
	photo = Photo.query.filter_by(id=photo_id).first()
	if photo:
		return send_file(os.path.join(current_app.instance_path, photo.full_url))
	else:
		abort(404)

@bp.route('/view/thumb/<int:photo_id>')
def view_thumb(photo_id):
	photo = Photo.query.filter_by(id=photo_id).first()
	if photo:
		return send_file(os.path.join(current_app.instance_path, photo.thumb_url))
	else:
		abort(404)
