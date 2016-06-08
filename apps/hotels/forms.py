from wtforms.fields import IntegerField, StringField, SelectField, FloatField, PasswordField, BooleanField, DateField
from wtforms import widgets, Form
from wtforms.validators import DataRequired, Email
from tables import Room, Country, session, POSITION_CHOICES, Hotel, City, UserProfile
from apps.users import utils


class UserReservationForm(Form):

	first_name = StringField(validators=[DataRequired()])
	last_name = StringField(validators=[DataRequired()])
	middle_name = StringField(validators=[DataRequired()])
	start_date_time = DateField(validators=[DataRequired()])
	end_date_time = DateField(validators=[DataRequired()])
