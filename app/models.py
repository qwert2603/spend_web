from app import db


class Record(db.Model):
    __tablename__ = 'records'

    uuid = db.Column(db.Text, primary_key=True)
    record_category_uuid = db.Column(db.Integer, db.ForeignKey('record_categories.uuid'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)
    kind = db.Column(db.Text, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    change_id = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)


class RecordCategory(db.Model):
    __tablename__ = 'record_categories'

    uuid = db.Column(db.Text, primary_key=True)
    record_type_id = db.Column(db.Integer, db.ForeignKey('record_types.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    records = db.relationship('Record', backref='record_category', lazy='dynamic')


class RecordType(db.Model):
    __tablename__ = 'record_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    record_categories = db.relationship('RecordCategory', backref='record_type', lazy='dynamic')


class DaySum:
    def __init__(self, row):
        self.date = row[0]
        self.sum = row[1]


class MonthSum:
    def __init__(self, row):
        self.year = int(row[0])
        self.month = int(row[1])
        self.sum = row[2]
