import os

from flask import (
	Blueprint, current_app, flash, g, redirect, render_template,
    request, session, url_for, jsonify, send_file, abort
)

bp = Blueprint('api.download', __name__, url_prefix='/api/download')

from itsyrealm.model.download import Download

def download_type_to_enum(value):
	if value == "launcher":
		return Download.TYPE_LAUNCHER
	elif value == "build":
		return Download.TYPE_BUILD
	elif value == "resource":
		return Download.TYPE_RESOURCE
	else:
		return None

@bp.route('/<string:download_type>/version')
@bp.route('/<string:download_type>/version/<string:version>')
def index(download_type, version=None):
	download_type = download_type_to_enum(download_type)
	if not download_type:
		abort(404)

	if not version:
		latest = Download.query.order_by(Download.id.desc()).first()
		version = latest.version
		
	result = []
	downloads = Download.query.filter_by(type=download_type, version=version).all()

	for download in downloads:
		result.append(download.serialize())

	return jsonify(result)

@bp.route('/<string:download_type>/get/<string:platform_id>')
@bp.route('/<string:download_type>/get/<string:platform_id>/<string:version>')
def view_full(download_type, platform_id, version=None):
	download_type = download_type_to_enum(download_type)
	if not download_type:
		abort(404)

	if not version:
		latest = Download.query.order_by(Download.id.desc()).first()
		version = latest.version

	download = Download.query.filter_by(type=download_type, platform=platform_id, version=version).first()
	if download:
		return send_file(os.path.join(current_app.instance_path, download.url), as_attachment=True, attachment_filename="itsyrealm.zip")
	else:
		abort(404)
