import datetime

from dateutil.relativedelta import relativedelta
from flask import render_template

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

    # @main.route('/add_record', methods=['GET', 'POST'])
    # def add_record():
    #     form = AddRecordForm()
    #     if form.validate_on_submit():
    #         db.session.add(Record(uuid=uuid.uuid4(), record_type_id=form.type.data, date=form.date.data,
    #                               time=form.time.data, kind=form.kind.data, value=form.value.data))
    #         return redirect(url_for('.index'))
    #     return render_template('main/add_record.html', form=form)
