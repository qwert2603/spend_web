from app import db
from app.utils import now_millis


class Record(db.Model):
    __tablename__ = 'records'

    uuid = db.Column(db.Text, primary_key=True)
    record_type_id = db.Column(db.Integer, db.ForeignKey('record_types.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    kind = db.Column(db.Text, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    updated = db.Column(db.Integer, nullable=False, default=now_millis)
    deleted = db.Column(db.Boolean, nullable=False, default=False)


class RecordType(db.Model):
    __tablename__ = 'record_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    records = db.relationship('Record', backref='record_type', lazy='dynamic')


class DaySum:
    def __init__(self, row):
        self.date = row[0]
        self.sum = row[1]
