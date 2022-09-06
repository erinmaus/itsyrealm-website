import os

from flask import (
	Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for
)
from flask_login import login_required

from itsyrealm.model.photo import Photo
from itsyrealm.forms.photoForm import PhotoForm
from itsyrealm.common.database import get_database

bp = Blueprint('admin_photos', __name__, url_prefix='/admin/photos')

@bp.route('/')
@login_required
def index():
	photos = Photo.query.order_by(Photo.id.desc()).all()

	return render_template("admin/photos/index.html", photos=photos)

def save_photo(type, file, photo_id):
	_, extension = os.path.splitext(file.filename)	
	local_filename = "photos/%s_%d%s" % (type, photo_id, extension)
	filename = "%s/%s" % (current_app.instance_path, local_filename)
	file.save(filename)

	return local_filename

def save_photo_form(photo, form):
	full = form.full.data
	if full:
		full_url = save_photo("full", full, photo.id)
	else:
		full_url = photo.full_url

	thumb = form.thumb.data
	if thumb:
		thumb_url = save_photo("thumb", thumb, photo.id)
	else:
		thumb_url = photo.thumb_url

	photo.full_url = full_url
	photo.thumb_url = thumb_url
	photo.title = form.title.data
	photo.description = form.description.data


@bp.route('/photo/<int:photo_id>', methods=('GET', 'POST'))
@login_required
def edit(photo_id):
	photo = Photo.query.filter_by(id=photo_id).first()
	if photo:
		form = PhotoForm()
		if request.method == 'GET':
			form.title.data = photo.title
			form.description.data = photo.description

		if form.validate_on_submit():
			save_photo_form(photo, form)

			db = get_database()
			db.session.add(photo)
			db.session.commit()

			flash("Photo updated.")
		elif request.method == 'POST':
			for field_name in form.errors:
				for field_error in form[field_name].errors:
					flash("%s: %s" % (form[field_name].description, field_error))

		return render_template("admin/photos/edit.html", photo=photo, form=form)

	else:
		flash("Photo not found.")
		return redirect(url_for("admin_photos.index", _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))

@bp.route('/photo/add', methods=('GET', 'POST'))
@login_required
def add():
	form = PhotoForm()

	if form.validate_on_submit():
		if not form.full.data or not form.thumb.data:
			flash("Both images are required.")
		else:
			db = get_database()

			photo = Photo()
			db.session.add(photo)
			db.session.flush()

			save_photo_form(photo, form)

			db.session.add(photo)
			db.session.commit()

			flash("Photo added.")

			return redirect(url_for("admin_photos.index", _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))
	elif request.method == 'POST':
		for field_name in form.errors:
			for field_error in form[field_name].errors:
				flash("%s: %s" % (form[field_name].description, field_error))

	return render_template("admin/photos/add.html", form=form)

@bp.route("/photo/delete/<int:photo_id>")
@login_required
def delete(photo_id):
	database = get_database()

	try:
		photo = Photo.query.filter_by(id=photo_id).first()
		if not photo:
			raise Exception("No photo.")

		os.remove(os.join(current_app.instance_path, download.thumb_url))
		os.remove(os.join(current_app.instance_path, download.full_url))

		database.session.delete(photo)
		database.session.commit()
	
		flash("Deleted photo.")
	except:
		flash("Failed to delete photo.")

	return redirect(url_for("photos.index", _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))
