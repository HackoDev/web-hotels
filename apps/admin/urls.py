from apps.admin.views import CountryAdminListView, CountryAddForm
from tornado.web import url

url_patterns = [
    url(r'/admin/countries/', CountryAdminListView, name='admin-countries-list'),
    url(r'/admin/countries/add/', CountryAddForm, name='admin-countries-add')
]
