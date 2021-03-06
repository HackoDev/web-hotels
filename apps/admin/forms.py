from wtforms.fields import IntegerField, StringField, SelectField, FloatField, PasswordField, BooleanField, DateField
from wtforms import widgets
from wtforms.validators import DataRequired, Email
from wtforms_tornado import Form
from tables import Room, Country, session, POSITION_CHOICES, Hotel, City, UserProfile
from apps.users import utils


class CountryAdminForm(Form):

    title = StringField(validators=[DataRequired()])


class CityAdminForm(Form):

    def __init__(self, *args, **kwargs):
        super(CityAdminForm, self).__init__(*args, **kwargs)
        self.country_id.choices = [(str(f.id), str(f)) for f in session.query(Country).all()]

    title = StringField("Название", validators=[DataRequired()])
    country_id = SelectField("Страна", validators=[DataRequired()])


class HotelAdminForm(Form):

    def __init__(self, *args, **kwargs):
        super(HotelAdminForm, self).__init__(*args, **kwargs)
        self.city_id.choices = [(str(f.id), str(f)) for f in session.query(City).all()]

    city_id = SelectField("Город", validators=[DataRequired()])
    title = StringField("Название", validators=[DataRequired()])
    description = StringField("Описание", validators=[DataRequired()], widget=widgets.TextArea())
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


class UserProfileForm(Form):

    first_name = StringField("Имя", validators=[DataRequired()])
    second_name = StringField("Фамилия", validators=[DataRequired()])
    middle_name = StringField("Отчество", validators=[DataRequired()])
    # auth info
    email = StringField("Email", validators=[Email(), DataRequired()])
    password1 = PasswordField("Пароль")
    password2 = PasswordField("Повторите пароль")

    is_staff = BooleanField("Статус персонала")

    def validate(self):
        success = super(UserProfileForm, self).validate()
        if self.password1.data != self.password2.data:
            success = False
            errors = self.errors.get('password1', [])
            errors.append("Пароли не совпадают")
            self.errors.update("password1", errors)
        return success

    @property
    def data(self):
        """ Override base data for create hash password """
        data = super(UserProfileForm, self).data
        if self.password1.data and self.password2.data:
            data.update({
                "password": utils.make_password(self.password1.data)
            })
        data.pop("password1")
        data.pop("password2")
        # raise ValueError(data)
        return data


class ReservationForm(Form):

    first_name = StringField("Имя", validators=[DataRequired()])
    last_name = StringField("Фамилия", validators=[DataRequired()])
    middle_name = StringField("Отчество", validators=[DataRequired()])
    start_date_time = DateField("Дата заселения", validators=[DataRequired()])
    end_date_time = DateField("Дата выеда", validators=[DataRequired()])
    room_id =  SelectField("Номер", validators=[DataRequired()])
    price = FloatField("По цене", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.room_id.choices = [(str(f.id), ": ".join([str(f.hotel()), str(f)])) for f in session.query(Room).all()]
