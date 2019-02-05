from itsyrealm.model.main import db

class Release(db.Model):
	TYPE_LAUNCHER = 0
	TYPE_BUILD    = 1
	TYPE_RESOURCE = 2

	TAG_ALPHA     = 0
	TAG_BETA      = 1
	TAG_RELEASE   = 2

	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.Integer, nullable=False)
	version_major = db.Column(db.Integer, nullable=False)
	version_minor = db.Column(db.Integer, nullable=False)
	version_revision = db.Column(db.Integer, nullable=False)
	version_tag = db.Column(db.Integer, nullable=False)
	patch_notes = db.Column(db.Text, nullable=True)

	downloads = db.relationship('Download', backref='release', cascade="all,delete")

	def get_type_string(type):
		if type == Release.TYPE_LAUNCHER:
			return "launcher"
		elif type == Release.TYPE_BUILD:
			return "build"
		elif type == Release.TYPE_RESOURCE:
			return "resource"

	def get_tag_string(type):
		if type == Release.TAG_ALPHA:
			return "alpha"
		elif type == Release.TAG_BETA:
			return "beta"
		elif type == Release.TAG_RELEASE:
			return "release"

	def get_tag_enum(tag):
		if tag == "alpha":
			return Release.TAG_ALPHA
		elif tag == "beta":
			return Release.TAG_BETA
		elif tag == "release":
			return Release.TAG_RELEASE

	def get_version_string(self):
		return "{}.{}.{}-{}".format(
			self.version_major,
			self.version_minor,
			self.version_revision,
			Release.get_tag_string(self.version_tag))

	def parse_version_string(version):
		major = 0
		minor = 0
		revision = 0
		tag = ""

		parts = version.split('.')
		if len(parts) == 3:
			major = int(parts[0])
			minor = int(parts[1])

			suffix = parts[2].split('-')

			if len(suffix) == 2:
				revision = int(suffix[0])
				tag = suffix[1].lower()

		return major, minor, revision, tag

	def get_latest_version():
		return Release.query.order_by(
			Release.version_major.desc(),
			Release.version_minor.desc(),
			Release.version_revision.desc(),
			Release.version_tag.desc()).first()

	def get_version(version):
		major, minor, revision, tag = Release.parse_version_string(version)
		return Release.query.filter_by(
			version_major=major,
			version_minor=minor,
			version_revision=revision,
			version_tag=Release.get_tag_enum(tag)).first()


	def serialize(self):
		release = {
			'id': self.id,
			'type': Release.get_type_string(self.type),
			'version': self.get_version_string(),
			'patchNotes': self.patch_notes
		}

		downloads = [];
		for download in self.downloads:
			downloads.append(download.serialize())

		release['downloads'] = downloads

		return release
