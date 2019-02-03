import os
import hashlib

from flask import (
	Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for
)
from flask_login import login_required

from itsyrealm.model.download import Download
from itsyrealm.forms.downloadForm import DownloadForm
from itsyrealm.common.database import get_database

bp = Blueprint('admin.downloads', __name__, url_prefix='/admin/downloads')

@bp.route('/')
@login_required
def index():
	downloads = Download.query.order_by(Download.id.desc()).all()

	return render_template("admin/downloads/index.html", downloads=downloads)

def save_download(type, file, download_id):
	_, extension = os.path.splitext(file.filename)	
	local_filename = "downloads/%s/%d%s" % (type, download_id, extension)
	filename = "%s/%s" % (current_app.instance_path, local_filename)
	file.save(filename)

	checksum = hashlib.sha512(file.read()).hexdigest()

	return local_filename, checksum

def save_download_form(download, form):
	binary = form.binary.data

	url, checksum = save_download(Download.get_type_string(int(download.type)), binary, download.id)
	download.url = url
	download.checksum = checksum

@bp.route('/download/<int:download_id>', methods=('GET', 'POST'))
@login_required
def edit(download_id):
	download = Download.query.filter_by(id=download_id).first()
	if download:
		form = DownloadForm()
		if request.method == 'GET':
			form.type.data = str(download.type)
			form.platform.data = download.platform
			form.version.data = download.version
			form.patch_notes.data = download.patch_notes

		if form.validate_on_submit():
			if form.binary.data:
				save_download_form(download, form)

			download.type = form.type.data
			download.platform = form.platform.data
			download.version = form.version.data
			download.patch_notes = form.patch_notes.data

			db = get_database()
			db.session.add(download)
			db.session.commit()

			flash("Download updated.")

		return render_template("admin/downloads/edit.html", download=download, form=form)

	else:
		flash("Download not found.")
		return redirect(url_for("admin.downloads.index"))

@bp.route('/download/add', methods=('GET', 'POST'))
@login_required
def add():
	form = DownloadForm()

	if form.validate_on_submit():
		if not form.binary.data:
			flash("Binary required.")
		else:
			db = get_database()

			download = Download()
			download.type = form.type.data
			download.platform = form.platform.data
			download.version = form.version.data
			download.patch_notes = form.patch_notes.data
			db.session.add(download)
			db.session.flush()

			save_download_form(download, form)

			db.session.add(download)
			db.session.commit()

			flash("Download added.")

			return redirect(url_for("admin.downloads.index"))

	return render_template("admin/downloads/add.html", form=form)

@bp.route("/download/delete/<int:download_id>")
@login_required
def delete(download_id):
	database = get_database()

	try:
		download = Download.query.filter_by(id=download_id).first()
		if not download:
			raise Exception("No download.")

		os.remove(os.path.join(current_app.instance_path, download.url))

		database.session.delete(download)
		database.session.commit()
	
		flash("Deleted download.")
	except Exception as e:
		flash("Failed to delete download.")
		flash(str(e))

	return redirect(url_for("admin.downloads.index"))
