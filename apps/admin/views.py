from apps.admin.forms import CountryAdminForm
from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler

from tables import BaseModel, UserPofile, Country, session


class Paginator(object):

    def __init__(self, query_set, page_size, current_page):
        if isinstance(current_page, basestring):
            if current_page.isdigit():
                current_page = int(current_page)
        self.page = current_page
        self.page_size = page_size
        self.query_set = query_set
        self.count = query_set.count()
        self.max_page = self.count / self.page_size
        print "Max page size: ", self.max_page
        if self.max_page > 0:
            self.max_page += int(self.count - self.max_page*self.page > 0)

        self.start_position = (self.page - 1)*self.page_size
        self.end_position = self.page*self.page_size

    def get_results(self):
        self.prev_page = None
        self.next_page = None
        print self.page
        print self.max_page
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


class BaseAdminView(RequestHandler):

    display_fields = []

    page_size = 10
    PAGE_ARGUMENT_NAME = "page"

    def get_paginated_list(self):
        page = self.get_argument(self.PAGE_ARGUMENT_NAME, "1")
        if not page.isdigit():
            page = 1
        return Paginator(session.query(self.model_class).filter(), self.page_size, page).get_results()

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
            ctx=self.get_paginated_list()
        )
        self.render("admin/list_view.html", **extra_params)


class CountryAdminListView(BaseAdminView):

    model_class = Country
    display_fields = ['id', 'title']


class CountryAddForm(RequestHandler):

    model_class = Country
    form_class = CountryAdminForm
    success_url = "admin-countries-list"

    @property
    def title(self):
        return self.model_class.Meta.verbose_name

    def post(self):
        form = self.form_class(self.request.arguments)
        if form.validate():
            country = Country(**form.data)
            session.add(country)
            session.commit()
            self.redirect(self.reverse_url(self.success_url))

        self.get(form=form)

    def get(self, form=None):
        extra_params = dict(
            opts={
                "model": self.model_class,
                "meta": self.model_class.Meta
            },
            title=self.title,
            form=form or self.form_class()
        )
        self.render("admin/add_view.html", **extra_params)


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