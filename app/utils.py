import datetime

from dateutil.relativedelta import relativedelta

from app import db


def get_sums_by_days_spends():
    start_date = datetime.date.today()
    start_date = start_date.replace(day=1)
    start_date = start_date + relativedelta(months=-1)
    sql = '''
        SELECT
          r.date,
          sum(r.value)
        FROM records r LEFT JOIN record_categories c ON c.uuid = r.record_category_uuid
        WHERE c.record_type_id=1 AND r.date >= '{}'
        GROUP BY r.date
        ORDER BY r.date;
    '''.format(start_date)
    from app.models import DaySum
    return [DaySum(row) for row in _execute_sql(sql)]


def get_sums_by_months_spends():
    sql = '''
        SELECT
          extract(YEAR FROM DATE)  y,
          extract(MONTH FROM DATE) m,
          sum(value)
        FROM records
        GROUP BY y, m
        ORDER BY y, m
    '''
    from app.models import MonthSum
    return [MonthSum(row) for row in _execute_sql(sql)]


def _execute_sql(sql):
    return db.engine.execute(sql)


def get_records_types_ids():
    from app.models import RecordType
    records_types = RecordType.query.all()
    result = set()
    for records_type in records_types:
        result.add(records_type.id)
    return result


month_names = [
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
]
