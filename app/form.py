from wtforms import DateField, IntegerField
from wtforms.widgets import Input


class DateInput(Input):
    input_type = 'date'


class DateFieldWidget(DateField):
    widget = DateInput()


class IntegerInput(Input):
    input_type = 'number'


class IntegerFieldWidget(IntegerField):
    widget = IntegerInput()
