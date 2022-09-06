import os

from flask import Flask
from flask_bootstrap import Bootstrap

def make_directories(path):
	try:
		os.makedirs(path)
	except:
		pass

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		MAX_CONTENT_LENGTH=128 * 1024 * 1024,
		SQLALCHEMY_TRACK_MODIFICATIONS=False,
		SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
		SECRET_KEY=os.environ.get('SECRET_KEY', None),
		SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI', None),
		PREFERRED_URL_SCHEME=os.environ.get('PREFERRED_URL_SCHEME', default='https')
	)

	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	make_directories(app.instance_path)
	make_directories(os.path.join(app.instance_path, "photos"))
	make_directories(os.path.join(app.instance_path, "downloads"))
	make_directories(os.path.join(app.instance_path, "downloads", "launcher"))
	make_directories(os.path.join(app.instance_path, "downloads", "resource"))
	make_directories(os.path.join(app.instance_path, "downloads", "build"))

	try:
		app.config.from_pyfile("settings.cfg")
	except:
		pass

	from itsyrealm.common.database import init_app as init_database
	init_database(app)

	from itsyrealm.common.auth import init_app as init_login
	init_login(app)

	Bootstrap(app)

	import itsyrealm.views.home as home
	app.register_blueprint(home.bp)

	import itsyrealm.views.admin.home as admin_home
	import itsyrealm.views.admin.downloads as admin_downloads
	import itsyrealm.views.admin.photos as admin_photos
	app.register_blueprint(admin_home.bp)
	app.register_blueprint(admin_downloads.bp)
	app.register_blueprint(admin_photos.bp)

	import itsyrealm.views.api.photo as api_photo
	import itsyrealm.views.api.download as api_download
	app.register_blueprint(api_photo.bp)
	app.register_blueprint(api_download.bp)

	return app
