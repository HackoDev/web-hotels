from wtforms.fields import IntegerField, StringField, SelectField, FloatField
from wtforms import widgets
from wtforms.validators import DataRequired
from wtforms_tornado import Form
from tables import Room, Country, session, POSITION_CHOICES, Hotel, City


class CountryAdminForm(Form):

    title = StringField(validators=[DataRequired()])#, label="Название".decode("utf-8"))


class CityAdminForm(Form):

    def __init__(self, *args, **kwargs):
        super(CityAdminForm, self).__init__(*args, **kwargs)
        self.country_id.choices = [(str(f.id), str(f)) for f in session.query(Country).all()]

    title = StringField("Название", validators=[DataRequired()])#, label="Название".decode("utf-8"))
    country_id = SelectField("Страна",validators=[DataRequired()])#label="Страна".decode("utf-8"))


class HotelAdminForm(Form):

    def __init__(self, *args, **kwargs):
        super(HotelAdminForm, self).__init__(*args, **kwargs)
        self.city_id.choices = [(str(f.id), str(f)) for f in session.query(City).all()]

    city_id = SelectField("Город", validators=[DataRequired()])
    title = StringField("Название" ,validators=[DataRequired()])#, label="Название".decode("utf-8"))
    position = SelectField("Количество звезд", choices=POSITION_CHOICES, validators=[DataRequired()])#label="Звездность".decode("utf-8"))


class RoomAdminForm(Form):

    def __init__(self, *args, **kwargs):
        super(RoomAdminForm, self).__init__(*args, **kwargs)
        self.hotel_id.choices = [(str(f.id), str(f)) for f in session.query(Hotel).all()]

    hotel_id = SelectField("Отель",validators=[DataRequired()])
    title = StringField("Название", validators=[DataRequired()])
    description = StringField("Краткое описание", widget=widgets.TextArea())


class RoomPriceAdminForm(Form):

    def __init__(self, *args, **kwargs):
        super(RoomPriceAdminForm, self).__init__(*args, **kwargs)
        self.room_id.choices = [(str(f.id), ": ".join([str(f.hotel()), str(f)])) for f in session.query(Room).all()]

    value = FloatField("Цена", validators=[DataRequired()])
    room_id = SelectField("Номер", validators=[DataRequired()])
