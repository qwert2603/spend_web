import time

from app import db


def get_sums_by_days_spends():
    sql = '''
        SELECT
          date,
          sum(value)
        FROM records
        WHERE record_type_id=1
        GROUP BY date
        ORDER BY date DESC;
    '''
    from app.models import DaySum
    return [DaySum(row) for row in _execute_sql(sql)]


def _execute_sql(sql):
    return db.engine.execute(sql)


def now_millis():
    return int(round(time.time() * 1000))


def get_records_types_ids():
    from app.models import RecordType
    records_types = RecordType.query.all()
    result = set()
    for records_type in records_types:
        result.add(records_type.id)
    return result
