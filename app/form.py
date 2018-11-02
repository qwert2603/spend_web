from wtforms import DateField, IntegerField, TimeField
from wtforms.widgets import Input


class DateInput(Input):
    input_type = 'date'


class DateFieldWidget(DateField):
    widget = DateInput()


class TimeInput(Input):
    input_type = 'time'


class TimeFieldWidget(TimeField):
    widget = TimeInput()


class IntegerInput(Input):
    input_type = 'number'


class IntegerFieldWidget(IntegerField):
    widget = IntegerInput()
