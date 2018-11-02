import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import Length, DataRequired, ValidationError

from app.form import DateFieldWidget, IntegerFieldWidget
from app.models import RecordType


class AddRecordForm(FlaskForm):
    type = SelectField('тип', coerce=int)
    date = DateFieldWidget('дата', validators=[DataRequired()], default=datetime.date.today())
    kind = StringField('вид', validators=[Length(1, 64)])
    value = IntegerFieldWidget('сумма', validators=[DataRequired()])
    submit = SubmitField('сохранить')

    def __init__(self, *args, **kwargs):
        super(AddRecordForm, self).__init__(*args, *kwargs)
        self.type.choices = [(t.id, t.name) for t in RecordType.query.all()]

    def validate_value(self, field):
        if field.data <= 0:
            raise ValidationError('value <= 0')
        if field.data > 100000:
            raise ValidationError('value > 100.000')
