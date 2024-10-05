from datetime import datetime

from ..extensions import db

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    name = db.Column(db.String(26), unique=True, nullable=False)
    purchase_at = db.Column(db.Date, nullable=True)
    expired_at = db.Column(db.Date, nullable=True)
    external_id = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Domain {self.name}>'