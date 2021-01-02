from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import SelectField, IntegerField, DateField, FloatField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from Proxy import app


class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    port = StringField('Port Number', validators=[DataRequired()])
    submit = SubmitField('Submit')
