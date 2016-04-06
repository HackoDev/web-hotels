from apps.admin.views import CountryAdminListView

url_patterns = [
    (r'/admin/countries/', CountryAdminListView)
]
