from apps.admin.forms import CountryAdminForm, CityAdminForm, HotelAdminForm, RoomAdminForm, RoomPriceAdminForm, UserProfileForm, ReservationForm
from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler
import tornado.web

from tables import BaseModel, UserProfile, Country, session, City, Hotel, Room, RoomPrice, Reservation
from settings import settings


def is_staff_user(method):
    """ Check permissions for current user. Only staff users """

    def wrapper(self, *args, **kwargs):
        user = int(self.get_current_user() or 0)
        is_admin = session.query(UserProfile).filter(UserProfile.id == user, UserProfile.is_staff == True).count() == 1
        if is_admin:
            return method(self, *args, **kwargs)
        return self.redirect(settings["login_url"] + "?next=" + self.request.uri)
    return wrapper


class Paginator(object):

    def __init__(self, query_set, page_size, current_page, order_by=None):
        if isinstance(current_page, str):
            if current_page.isdigit():
                current_page = int(current_page)
        if order_by is not None:
            self.order_by = order_by
        self.prev_page = None
        self.next_page = None
        self.page = current_page
        self.page_size = page_size
        self.query_set = query_set.order_by(*self.order_by)
        self.count = query_set.count()
        self.max_page = self.count / self.page_size
        if self.max_page > 0:
            self.max_page += int(self.count - self.max_page*self.page > 0)

        if self.max_page == 0 and self.count > 0:
            self.max_page += 1
        self.start_position = (self.page - 1)*self.page_size
        self.end_position = self.page*self.page_size

    def get_results(self):
        if self.page > 1:
            self.prev_page = self.page - 1
        if self.page + 1 <= self.max_page:
            self.next_page = self.page + 1
        return dict(
            objects_list=self.query_set.slice(self.start_position, self.end_position),
            page=self.page,
            max_page=int(self.max_page or 0),
            next_page=self.next_page,
            prev_page=self.prev_page
        )


class BaseAdminListView(RequestHandler):

    display_fields = []

    page_size = 10
    PAGE_ARGUMENT_NAME = "page"
    tab_active = None
    order_fields = ['-id']

    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def admin_add_url(self):
        raise NotImplementedError("No set add url")

    @property
    def admin_list_url(self):
        raise NotImplementedError("No set add url")

    @property
    def order_by(self):
        return map(
            lambda x: getattr(self.model_class, x[1:]).desc() if x.startswith('-') else getattr(self.model_class, x),
            self.order_fields
        )

    def data_received(self, chunk):
        raise ValueError('error implementation')

    def get_paginated_list(self):
        page = self.get_argument(self.PAGE_ARGUMENT_NAME, "1")
        if not page.isdigit():
            page = 1
        return Paginator(session.query(self.model_class).filter(), self.page_size, page,
                         order_by=self.order_by).get_results()

    @property
    def model_class(self):
        raise NotImplementedError("Not setted model value")

    @property
    def title(self):
        return self.model_class.Meta.verbose_name_plural

    @tornado.web.authenticated
    @is_staff_user
    def get(self):
        extra_params = dict(
            opts={
                "model": self.model_class,
                "meta": self.model_class.Meta
            },
            title=self.title,
            has_display_fields=self.display_fields.__len__(),
            display_fields=self.display_fields,
            ctx=self.get_paginated_list(),
            tab_active=self.tab_active
        )
        self.render("admin/list_view.html", **extra_params)


class BaseAdminAddChangeView(RequestHandler):

    tab_active = None

    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def model_class(self):
        raise NotImplementedError("Not set model class")

    @property
    def form_class(self):
        raise NotImplementedError("Not set form class")

    @property
    def success_url(self):
        raise NotImplementedError("Not set success url")

    def get_success_url(self):
        # TODO: get success url
        to = self.get_argument('to', None)
        # if to is not None:
        #     return to
        return self.reverse_url(self.success_url)

    @property
    def title(self):
        return self.model_class.Meta.verbose_name

    def get_object(self, pk):
        if pk is None:
            return self.model_class()
        try:
            self.object = session.query(self.model_class).filter(self.model_class.id == pk).one()
        except:
            self.set_status(400)
            self.finish("<html><body>not found</body></html>")
        else:
            return self.object

    def bind_data(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)

    @tornado.web.authenticated
    @is_staff_user
    def post(self, pk=None):
        form = self.form_class(self.request.arguments)
        if form.validate():
            self.object = self.get_object(pk)
            self.bind_data(self.object, form.data)
            session.add(self.object)
            session.commit()
            self.redirect(self.get_success_url())
        else:
            print("invalid form")
        self.get(form=form, pk=pk)

    def get_form_kwargs(self):
        return self.object.to_dict()

    @tornado.web.authenticated
    @is_staff_user
    def get(self, form=None, pk=None):
        print(self.get_current_user())
        self.object = self.get_object(pk)
        extra_params = dict(
            opts={
                "model": self.model_class,
                "meta": self.model_class.Meta
            },
            instance=self.object,
            title=self.title,
            form=form or self.form_class(**self.get_form_kwargs()),
            to=self.request.headers.get("Referer") or self.reverse_url(self.success_url),
            tab_active=self.tab_active
        )
        self.render("admin/add_view.html", **extra_params)


class BaseAdminDeleteView(RequestHandler):

    tab_active = None

    @property
    def model_class(self):
        raise NotImplementedError("Not set model class")

    @property
    def success_url(self):
        raise NotImplementedError("Not set success url")

    @property
    def title(self):
        return self.model_class.Meta.verbose_name

    def get_object(self, pk):
        try:
            self.object = session.query(self.model_class).filter(self.model_class.id == pk).one()
        except:
            self.set_status(400)
            self.finish("<html><body>not found</body></html>")
        else:
            return self.object

    def post(self, pk):
        self.object = self.get_object(pk)
        session.delete(self.object)
        self.redirect(self.reverse_url(self.success_url))

    def get(self, pk):
        self.object = self.get_object(pk)
        extra_params = dict(
            opts={
                "model": self.model_class,
                "meta": self.model_class.Meta
            },
            instance=self.object,
            title=self.title,
            to=self.reverse_url(self.success_url),
            tab_active=self.tab_active
        )
        self.render("admin/delete.html", **extra_params)


# define admin classes


class IndexView(RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")

    @tornado.web.authenticated
    @is_staff_user
    def get(self):
        ctx = dict(
            title="Администрирование",
            tab_active=None
        )
        self.render("admin/index.html", **ctx)


class CountryAdminListView(BaseAdminListView):
    """ Admin country list view """

    model_class = Country
    display_fields = ['id', 'title']    
    tab_active = 'country'
    order_fields = ['title']


class CityAdminListView(BaseAdminListView):
    """ Admin city list view """

    model_class = City
    display_fields = ['id', 'title', 'country']
    tab_active = 'city'
    order_fields = ['title']


class HotelAdminListView(BaseAdminListView):
    """ Admin hotel list view """

    model_class = Hotel
    display_fields = ['id', 'title', 'position', 'city']
    tab_active = 'hotel'
    order_fields = ['title']


class RoomAdminListView(BaseAdminListView):
    """ Admin hotel list view """

    model_class = Room
    display_fields = ['id', 'title', 'hotel', 'price']
    tab_active = 'room'



class RoomPriceAdminListView(BaseAdminListView):
    """ Admin hotel list view """

    model_class = RoomPrice
    display_fields = ['id', 'value', 'room']
    tab_active = 'room-price'



class UserAdminListView(BaseAdminListView):
    """ Admin user list view """

    model_class = UserProfile
    display_fields = ['id', 'first_name', 'second_name', 'middle_name', 'email', 'is_staff']
    tab_active = 'user'



class ReservationAdminListView(BaseAdminListView):
    """ Admin user list view """

    model_class = Reservation
    display_fields = ['id', 'first_name', 'last_name', 'middle_name', 'start_date_time', 'end_date_time']
    tab_active = 'reservation'


class CountryAddChangeView(BaseAdminAddChangeView):
    """ Admin country add and change view """

    model_class = Country
    form_class = CountryAdminForm
    success_url = "admin:country-list"
    tab_active = 'country'


class CityAddChangeView(BaseAdminAddChangeView):
    """ Admin city add and change view """

    model_class = City
    form_class = CityAdminForm
    success_url = "admin:city-list"
    tab_active = 'city'


class HotelAddChangeView(BaseAdminAddChangeView):
    """ Admin hotel add and change view """

    model_class = Hotel
    form_class = HotelAdminForm
    success_url = "admin:hotel-list"
    tab_active = 'hotel'


class RoomAddChangeView(BaseAdminAddChangeView):
    """ Admin hotel add and change view """

    model_class = Room
    form_class = RoomAdminForm
    success_url = "admin:room-list"
    tab_active = 'room'


class RoomPriceAddChangeView(BaseAdminAddChangeView):
    """ Admin room price add and change view """

    model_class = RoomPrice
    form_class = RoomPriceAdminForm
    success_url = "admin:room-price-list"
    tab_active = 'room-price'



class UserAddChangeView(BaseAdminAddChangeView):
    """ Admin user add and change view """

    model_class = UserProfile
    form_class = UserProfileForm
    success_url = "admin:user-list"
    tab_active = 'user'



class ReservationAddChangeView(BaseAdminAddChangeView):
    """ Admin user add and change view """

    model_class = Reservation
    form_class = ReservationForm
    success_url = "admin:reservation-list"
    tab_active = 'reservation'


class CityDeleteView(BaseAdminDeleteView):
    """ Admin city delete view """

    model_class = City
    success_url = 'admin:city-list'
    tab_active = 'city'


class RoomDeleteView(BaseAdminDeleteView):
    """ Admin city delete view """

    model_class = Room
    success_url = 'admin:room-list'
    tab_active = 'room'


class CountryDeleteView(BaseAdminDeleteView):
    """ Admin country delete view """

    model_class = Country
    success_url = 'admin:country-list'
    tab_active = 'country'


class HotelDeleteView(BaseAdminDeleteView):
    """ Admin hotel delete view """

    model_class = Hotel
    success_url = 'admin:hotel-list'
    tab_active = 'hotel'


class RoomPriceDeleteView(BaseAdminDeleteView):
    """ Admin room price delete view """

    model_class = RoomPrice
    success_url = 'admin:room-price-list'
    tab_active = 'room-price'



class UserDeleteView(BaseAdminDeleteView):
    """ Admin user delete view """

    model_class = UserProfile
    success_url = 'admin:user-list'
    tab_active = 'user'


class ReservationDeleteView(BaseAdminDeleteView):
    """ Admin user delete view """

    model_class = Reservation
    success_url = 'admin:reservation-list'
    tab_active = 'reservation'
