# -*- coding: utf-8 -*-
from wtforms.fields import IntegerField, StringField, SelectField
from wtforms import widgets
from wtforms.validators import DataRequired
from wtforms_tornado import Form
from tables import Room, Country, session, POSITION_CHOICES, Hotel, City


class CountryAdminForm(Form):

    title = StringField(validators=[DataRequired()])#, label="Название".decode("utf-8"))


class CityAdminForm(Form):

    def __init__(self, *args, **kwargs):
        super(CityAdminForm, self).__init__(*args, **kwargs)
        self.country_id.choices = [(unicode(f.id), unicode(f)) for f in session.query(Country).all()]

    title = StringField(validators=[DataRequired()])#, label="Название".decode("utf-8"))
    country_id = SelectField(validators=[DataRequired()])#label="Страна".decode("utf-8"))


class HotelAdminForm(Form):

    def __init__(self, *args, **kwargs):
        super(HotelAdminForm, self).__init__(*args, **kwargs)
        self.city_id.choices = [(unicode(f.id), unicode(f)) for f in session.query(City).all()]

    city_id = SelectField(validators=[DataRequired()])
    title = StringField(validators=[DataRequired()])#, label="Название".decode("utf-8"))
    position = SelectField(choices=POSITION_CHOICES, validators=[DataRequired()])#label="Звездность".decode("utf-8"))


class RoomAdminForm(Form):

    def __init__(self, *args, **kwargs):
        super(RoomAdminForm, self).__init__(*args, **kwargs)
        self.hotel_id.choices = [(unicode(f.id), unicode(f)) for f in session.query(Hotel).all()]

    hotel_id = SelectField(validators=[DataRequired()])
    title = StringField(validators=[DataRequired()])
