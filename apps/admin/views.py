from apps.admin.forms import CountryAdminForm
from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler

from tables import BaseModel, UserPoile, Country, session


class BaseAdminView(RequestHandler):

    display_fields = []

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
            objects=session.query(self.model_class).all()
        )
        self.render("admin/list_view.html", **extra_params)


class CountryAdminListView(BaseAdminView):

    model_class = Country
    display_fields = ['id', 'title']


class CountryAddForm(RequestHandler):

    model_class = Country
    form_class = CountryAdminForm

    @property
    def title(self):
        return self.model_class.Meta.verbose_name

    def post(self):
        form = self.form_class(self.request.arguments)
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
    #     print(session.query(UserPoile).all())
    #     if self.get_argument('create_user', False):
    #         user = UserPoile(first_name=u"Evgeniy", second_name=u"Hacko", middle_name=u"Gennadievich", email="hacko@nicecode.biz")
    #         user.set_password('password')
    #         session.add(user)
    #         try:
    #             session.commit()
    #         except Exception, e:
    #             self.write(u"Exception: %s" % e.message)
    #             session.rollback()
    #     self.write("Hotels index view")