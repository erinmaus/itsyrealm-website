from itsyrealm.model.main import db

class Download(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	release_id = db.Column(db.Integer, db.ForeignKey('release.id'), nullable=False)
	url = db.Column(db.Text)
	checksum = db.Column(db.Text)
	platform = db.Column(db.Text, nullable=False)
	num_downloads = db.Column(db.Integer)

	def serialize(self):
		return {
			'id': self.id,
			'platform': self.platform,
			'checksum': self.checksum
		}
