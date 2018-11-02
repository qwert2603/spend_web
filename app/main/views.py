import uuid

from flask import render_template, redirect, url_for

from app import db
from app.main import main
from app.main.forms import AddRecordForm
from app.models import Record
from app.utils import get_sums_by_days_spends


@main.route('/')
def index():
    records = Record.query \
        .order_by(Record.date.desc(), Record.time.desc().nullslast(), Record.record_type_id, Record.uuid) \
        .all()
    return render_template('main/index.html', records=records)


@main.route('/by_days_spends')
def by_days_spends():
    return render_template('main/by_days_spends.html', day_sums=get_sums_by_days_spends())


@main.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form = AddRecordForm()
    if form.validate_on_submit():
        db.session.add(Record(uuid=uuid.uuid4(), record_type_id=form.type.data, date=form.date.data,
                              time=form.time.data, kind=form.kind.data, value=form.value.data))
        return redirect(url_for('.index'))
    return render_template('main/add_record.html', form=form)
