from apps.admin.forms import CountryAdminForm, CityAdminForm, HotelAdminForm, RoomAdminForm
from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler

from tables import BaseModel, UserProfile, Country, session, City, Hotel, Room


class Paginator(object):

    def __init__(self, query_set, page_size, current_page, order_by=None):
        if isinstance(current_page, basestring):
            if current_page.isdigit():
                current_page = int(current_page)
        if order_by is not None:
            self.order_by = order_by
        else:
            self.order_by = Country.id.desc()
        self.prev_page = None
        self.next_page = None
        self.page = current_page
        self.page_size = page_size
        self.query_set = query_set.order_by(self.order_by)
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
            max_page=self.max_page,
            next_page=self.next_page,
            prev_page=self.prev_page
        )


class BaseAdminListView(RequestHandler):

    display_fields = []

    page_size = 10
    PAGE_ARGUMENT_NAME = "page"
    tab_active = None

    @property
    def admin_add_url(self):
        raise NotImplementedError("No set add url")

    @property
    def admin_list_url(self):
        raise NotImplementedError("No set add url")

    @property
    def order_by(self):
        return self.model_class.id.desc()

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

    def post(self, pk=None):
        form = self.form_class(self.request.arguments)
        if form.validate():
            self.object = self.get_object(pk)
            self.bind_data(self.object, form.data)
            session.add(self.object)
            session.commit()
            self.redirect(self.get_success_url())
        else:
            print "invalid form"
        self.get(form=form, pk=pk)

    def get_form_kwargs(self):
        return self.object.to_dict()

    def get(self, form=None, pk=None):
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


class CountryAdminListView(BaseAdminListView):
    """ Admin country list view """

    model_class = Country
    display_fields = ['id', 'title']
    tab_active = 'country'


class CityAdminListView(BaseAdminListView):
    """ Admin city list view """

    model_class = City
    display_fields = ['id', 'title', 'country']
    tab_active = 'city'


class HotelAdminListView(BaseAdminListView):
    """ Admin hotel list view """

    model_class = Hotel
    display_fields = ['id', 'title', 'position', 'city']
    tab_active = 'hotel'


class RoomAdminListView(BaseAdminListView):
    """ Admin hotel list view """

    model_class = Room
    display_fields = ['id', 'title', 'hotel']
    tab_active = 'room'


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


# class CountryChangeView(BaseAdminChangeView):

# class IndexHandler(BaseAdminView):

    # def get(self):
    #     print(session.query(UserPofile).all())
    #     if self.get_argument('create_user', False):
    #         user = UserPofile(first_name=u"Evgeniy", second_name=u"Hacko", middle_name=u"Gennadievich", email="hacko@nicecode.biz")
    #         user.set_password('password')
    #         session.add(user)
    #         try:
    #             session.commit()
    #         except Exception, e:
    #             self.write(u"Exception: %s" % e.message)
    #             session.rollback()
    #     self.write("Hotels index view")