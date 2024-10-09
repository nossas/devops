from datetime import datetime

from ..extensions import db, bonde_api


class Domain(db.Model):
    __tablename__ = "domains"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    name = db.Column(db.String(26), unique=True, nullable=False)
    purchase_at = db.Column(db.Date, nullable=True)
    expired_at = db.Column(db.Date, nullable=True)

    has_manage_dns = db.Column(db.Boolean(), default=True)
    hosted_zone_id = db.Column(db.String(140), nullable=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)

    def __repr__(self):
        return f'<Domain {self.name}>'


class Site(db.Model):
    __tablename__ = "sites"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    name = db.Column(db.String(26), unique=True, nullable=False)
    community_id = db.Column(db.Integer)

    domains = db.relationship('Domain', backref="site", lazy=True)

    def __repr__(self):
        return f'<Site {self.name}>'
    
    @property
    def community(self):
        return bonde_api.get_community_by_id(self.community_id)