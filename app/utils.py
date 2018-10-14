from app import db
from app.models import DaySum


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
    return [DaySum(row) for row in _execute_sql(sql)]


def _execute_sql(sql):
    return db.engine.execute(sql)
