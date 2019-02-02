from itsyrealm.model.main import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Text, nullable=False, unique=True)
	password_hash = db.Column(db.Text, nullable=False)
