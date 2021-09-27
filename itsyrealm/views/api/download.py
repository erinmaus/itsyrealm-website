import os

from flask import (
	Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for, jsonify, send_file, abort
)

bp = Blueprint('api_download', __name__, url_prefix='/api/download')

from itsyrealm.common.database import get_database
from itsyrealm.model.download import Download
from itsyrealm.model.release import Release

def download_type_to_enum(value):
	if value == "launcher":
		return Release.TYPE_LAUNCHER
	elif value == "build":
		return Release.TYPE_BUILD
	elif value == "resource":
		return Release.TYPE_RESOURCE
	else:
		return None

@bp.route('/<string:download_type>/version')
@bp.route('/<string:download_type>/version/<string:version>')
def index(download_type, version=None):
	download_type = download_type_to_enum(download_type)
	if download_type == None:
		abort(404)

	latest = None
	if not version:
		latest = Release.get_latest_version(download_type)
	else:
		try:
			latest = Release.get_version(download_type, version)
		except:
			pass
		
	if not latest:
		abort(404)

	return jsonify(latest.serialize())

@bp.route('/<string:download_type>/get/<string:platform_id>')
@bp.route('/<string:download_type>/get/<string:platform_id>/<string:version>')
def get(download_type, platform_id, version=None):
	download_type = download_type_to_enum(download_type)
	if download_type == None:
		abort(404)

	release = None
	if not version:
		release = Release.get_latest_version(download_type)
	else:
		try:
			release = Release.get_version(download_type, version)
		except:
			pass

	if not release:
		abort(404)

	filename = None
	if download_type == Release.TYPE_LAUNCHER:
		filename = "launcher.exe"
	elif download_type == Release.TYPE_BUILD:
		filename = "itsyrealm.zip"
	elif download_type == Release.TYPE_RESOURCE:
		filename = "itsyrealm.love"

	for download in release.downloads:
		if download.platform == platform_id:
			if not download.num_downloads:
				download.num_downloads = 1
			else:
				download.num_downloads += 1

			db = get_database()
			db.session.add(download)
			db.session.commit()

			return send_file(os.path.join(current_app.instance_path, download.url), cache_timeout=0, as_attachment=True, attachment_filename=filename)
			
	abort(404)
