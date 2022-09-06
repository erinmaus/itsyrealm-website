import os
import hashlib

from flask import (
	Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for
)
from flask_login import login_required

from itsyrealm.common.database import get_database
from itsyrealm.model.download import Download
from itsyrealm.model.release import Release
from itsyrealm.forms.downloadForm import DownloadForm
from itsyrealm.forms.releaseForm import ReleaseForm

bp = Blueprint('admin_downloads', __name__, url_prefix='/admin/downloads')

@bp.route('/')
@login_required
def index():
	releases = Release.query.order_by(Release.id.desc()).all()

	return render_template("admin/downloads/index.html", releases=releases)

@bp.route('/release/add', methods=('GET', 'POST'))
@login_required
def add_release():
	form = ReleaseForm()

	if form.validate_on_submit():
		db = get_database()

		release = Release()
		release.type = form.type.data
		release.version_major = form.version_major.data
		release.version_minor = form.version_minor.data
		release.version_revision = form.version_revision.data
		release.version_tag = form.version_tag.data
		release.patch_notes = form.patch_notes.data
		db.session.add(release)
		db.session.commit()

		flash("Release added.")

		return redirect(url_for("admin_downloads.edit_release",release_id=release.id, _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))

	return render_template("admin/downloads/add_release.html", form=form)

@bp.route('/release/edit/<int:release_id>', methods=('GET', 'POST'))
@login_required
def edit_release(release_id):
	release = Release.query.filter_by(id=release_id).first()
	if not release:
		flash("Invalid release.")
		return redirect(url_for("admin_downloads.index", _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))

	form = ReleaseForm()
	if request.method == 'GET':
		 form.type.data = str(release.type)
		 form.version_major.data = release.version_major
		 form.version_minor.data = release.version_minor
		 form.version_revision.data = release.version_revision
		 form.version_tag.data = str(release.version_tag)
		 form.patch_notes.data = release.patch_notes
	if form.validate_on_submit():
		db = get_database()

		release.type = form.type.data
		release.version_major = form.version_major.data
		release.version_minor = form.version_minor.data
		release.version_revision = form.version_revision.data
		release.version_tag = form.version_tag.data
		release.patch_notes = form.patch_notes.data
		db.session.add(release)
		db.session.commit()

		flash("Release updated.")

	return render_template("admin/downloads/edit_release.html", form=form, release=release)

def do_save_download(type, file, download_id):
	_, extension = os.path.splitext(file.filename)	
	local_filename = "downloads/%s/%d%s" % (type, download_id, extension)
	filename = "%s/%s" % (current_app.instance_path, local_filename)
	file.save(filename)

	checksum = hashlib.sha512(file.read()).hexdigest()

	return local_filename, checksum

def do_delete_download(download_id):
	download = Download.query.filter_by(id=download_id).first()
	if not download:
		raise Exception("No download.")

	try:
		os.remove(os.path.join(current_app.instance_path, download.url))
	except:
		pass

def save_download_form(release, download, form):
	binary = form.binary.data

	url, checksum = do_save_download(Release.get_type_string(int(release.type)), binary, download.id)
	download.url = url
	download.checksum = checksum

@bp.route('/download/<int:download_id>', methods=('GET', 'POST'))
@login_required
def edit_download(download_id):
	download = Download.query.filter_by(id=download_id).first()
	if download:
		form = DownloadForm()
		if request.method == 'GET':
			form.platform.data = download.platform

		if form.validate_on_submit():
			if form.binary.data:
				save_download_form(download.release, download, form)

			download.platform = form.platform.data

			db = get_database()
			db.session.add(download)
			db.session.commit()

			flash("Download updated.")

			return redirect(url_for("admin_downloads.edit_release", release_id=download.release_id, _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))

		return render_template("admin/downloads/edit_download.html", download=download, form=form)

	else:
		flash("Download not found.")
		return redirect(url_for("admin_downloads.index", _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))

@bp.route('/download/add/<int:release_id>', methods=('GET', 'POST'))
@login_required
def add_download(release_id):
	release = Release.query.filter_by(id=release_id).first()
	if not release:
		flash("Invalid release.")
		return redirect(url_for("admin_downloads.index", _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))

	form = DownloadForm()
	if form.validate_on_submit():
		if not form.binary.data:
			flash("Binary required.")
		else:
			db = get_database()

			download = Download()
			download.release_id = release_id
			download.platform = form.platform.data
			db.session.add(download)
			db.session.flush()

			save_download_form(release, download, form)

			db.session.add(download)
			db.session.commit()

			flash("Download added.")

			return redirect(url_for("admin_downloads.edit_release", release_id=release_id, _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))

	return render_template("admin/downloads/add_download.html", form=form)

@bp.route("/download/delete/<int:download_id>")
@login_required
def delete_download(download_id):
	database = get_database()

	download = Download.query.filter_by(id=download_id).first()

	try:
		do_delete_download(download_id)

		database.session.delete(download)
		database.session.commit()

		flash("Deleted download.")
	except Exception as e:
		flash("Failed to delete download: " + str(e))

	if download:
		return redirect(url_for("admin_releases.edit_release", release_id=download_id.release_id, _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))
	else:
		return redirect(url_for("admin_downloads.index", _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))

@bp.route("/release/delete/<int:release_id>")
@login_required
def delete_release(release_id):
	database = get_database()

	release = Release.query.filter_by(id=release_id).first()
	if release:
		for download in release.downloads:
			try:
				do_delete_download(download.id)
			except:
				pass
		
		database.session.delete(release)
		database.session.commit()

		flash("Deleted release.")
	else:
		flash("Failed to delete release.")

	return redirect(url_for("admin_downloads.index", _external=True, _scheme=current_app.config.get('PREFERRED_URL_SCHEME')))
