from itsyrealm.model.main import db

class Download(db.Model):
	TYPE_LAUNCHER = 0
	TYPE_BUILD    = 1
	TYPE_RESOURCE = 2

	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.Integer, nullable=False)
	platform = db.Column(db.Text, nullable=False)
	version = db.Column(db.Text, nullable=True)
	patch_notes = db.Column(db.Text, nullable=True)
	checksum = db.Column(db.Text)
	url = db.Column(db.Text)

	def get_type_string(type):
		if type == Download.TYPE_LAUNCHER:
			return "launcher"
		elif type == Download.TYPE_BUILD:
			return "build"
		elif type == Download.TYPE_RESOURCE:
			return "resource"
