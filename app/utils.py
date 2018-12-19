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
        WHERE c.record_type_id = 1 AND r.date >= '{}' AND NOT r.deleted
        GROUP BY r.date
        ORDER BY r.date;
    '''.format(start_date)
    from app.models import DaySum
    return [DaySum(row) for row in _execute_sql(sql)]


def get_sums_by_months_spends():
    sql = '''
        SELECT
          extract(YEAR FROM r.date)  y,
          extract(MONTH FROM r.date) m,
          sum(r.value)
        FROM records r LEFT JOIN record_categories c ON c.uuid = r.record_category_uuid
        WHERE c.record_type_id = 1 AND NOT r.deleted
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


def get_sums_by_categories_month(year, record_type_id):
    # { category_uuid: { month : sum } }
    # month = -1 means sum for whole year.
    # category_uuid = '_all' means sum for all categories.
    sql = '''
        SELECT
          record_category_uuid,
          extract(MONTH FROM r.date) mnth,
          sum(r.value)
        FROM (SELECT
                uuid,
                name
              FROM record_categories
              WHERE record_type_id = {}
              ORDER BY name) c LEFT JOIN records r ON c.uuid = r.record_category_uuid
        WHERE extract(YEAR FROM r.date) = {} AND NOT r.deleted
        GROUP BY record_category_uuid, mnth;
    '''.format(record_type_id, year)
    result = dict()
    result['_all'] = dict()
    result['_all'][-1] = 0
    for i in range(1, 13): result['_all'][i] = 0
    for row in _execute_sql(sql):
        category_uuid = row[0]
        month = int(row[1])
        sum = int(row[2])
        if result.get(category_uuid) is None:
            result[category_uuid] = dict()
            result[category_uuid][-1] = 0
        result[category_uuid][month] = sum
        result[category_uuid][-1] += sum
        result['_all'][month] += sum
        result['_all'][-1] += sum
    return result


def get_years():
    sql = '''
        SELECT DISTINCT
          extract(YEAR FROM date) y
        FROM records
        ORDER BY y
    '''
    return [int(row[0]) for row in _execute_sql(sql)]


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
