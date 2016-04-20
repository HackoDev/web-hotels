from wtforms.fields import IntegerField, StringField
from wtforms.validators import DataRequired
from wtforms_tornado import Form
from tables import Room


class CountryAdminForm(Form):

    title = StringField(validators=[DataRequired()])
