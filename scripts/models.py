from scripts.main import db

class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(10), nullable=False)