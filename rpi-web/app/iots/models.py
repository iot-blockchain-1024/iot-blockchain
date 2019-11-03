from datetime import datetime

from sqlalchemy import inspect

from .. import db


class IoTs(db.Model):
    __tablename__ = 'iots'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    hmt = db.Column(db.String(20), nullable=False)
    tmp = db.Column(db.String(20), nullable=False)
    ppm = db.Column(db.String(20), nullable=False)
    lx = db.Column(db.String(20), nullable=False)
    ld = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.String(20), nullable=False)
    device = db.Column(db.String(20), nullable=False)

    def __init__(self, hmt=None, tmp=None, ppm=None, lx=None, ld=None, date=None, time=None, timestamp=None, device=None):
        self.hmt = hmt
        self.tmp = tmp
        self.ppm = ppm
        self.lx = lx
        self.ld = ld
        self.date = date
        self.time = time
        self.timestamp = timestamp
        self.device = device

    def to_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
