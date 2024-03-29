import datetime

from dateutil.relativedelta import relativedelta
from flask import render_template, request, abort

from sqlalchemy import func

from app import db
from app.main import main
from app.models import Record, RecordCategory, RecordType
from app.utils import get_sums_by_days_spends, get_sums_by_months_spends, get_years, get_sums_by_categories_month
from config import Config


@main.route('/')
def index():
    start_date = datetime.date.today()
    start_date = start_date.replace(day=1)
    start_date = start_date + relativedelta(months=-1)

    records = Record.query \
        .join(RecordCategory, Record.record_category_uuid == RecordCategory.uuid) \
        .filter(RecordCategory.user_id == Config.records_user_id(), Record.date >= start_date,
                Record.deleted == False) \
        .order_by(Record.date.desc(), Record.time.desc().nullslast(), RecordCategory.name.desc(), Record.kind.desc(),
                  Record.uuid.desc()) \
        .all()
    return render_template('main/index.html', records=records)


@main.route('/by_days_spends')
def by_days_spends():
    return render_template('main/by_days_spends.html', day_sums=get_sums_by_days_spends())


@main.route('/by_months_spends')
def by_months_spends():
    return render_template('main/by_months_spends.html', month_sums=get_sums_by_months_spends())


@main.route('/by_categories')
def by_categories():
    return render_template('main/by_categories.html', years=get_years())


@main.route('/by_categories/<int:year>/<int:record_type_id>')
def by_categories_table(year, record_type_id):
    record_type = RecordType.query.get_or_404(record_type_id)
    categories = record_type.record_categories \
        .filter(RecordCategory.user_id == Config.records_user_id()) \
        .order_by(RecordCategory.name) \
        .all()
    return render_template('main/by_categories_table.html', year=year, record_type_id=record_type_id,
                           categories=categories, title='суммы по категориям. {} / {}'.format(year, record_type.name),
                           sums_by_categories_month=get_sums_by_categories_month(year, record_type_id))


@main.route('/current_month')
def current_month():
    d = datetime.date.today()
    d = d + relativedelta(months=1)
    d = d.replace(day=1)
    d = d + relativedelta(days=-1)
    total_days = d.day

    day = request.args.get('day', type=int)
    if day is not None and (day < 1 or day > total_days):
        abort(400)
    if day is None:
        day = datetime.date.today().day

    categories = []
    limits = {}
    spent = {}

    with open("month_limits.txt", 'r') as month_limits_file:
        for line in month_limits_file.readlines():
            split = line.split(" ")
            categories.append(split[0])
            limits[split[0]] = int(split[1])
            spent[split[0]] = 0

    start_date = datetime.date.today()
    start_date = start_date.replace(day=1)

    record_categories = db.session.query(RecordCategory.name, func.sum(Record.value)) \
        .filter(Record.record_category_uuid == RecordCategory.uuid, RecordCategory.user_id == Config.records_user_id(),
                Record.date >= start_date, RecordCategory.record_type_id == 1, Record.deleted == False) \
        .group_by(RecordCategory.name) \
        .all()

    for c in record_categories:
        spent[c[0]] = c[1]

    return render_template('main/current_month.html', total_days=total_days, day=day,
                           categories=categories, limits=limits, spent=spent)
