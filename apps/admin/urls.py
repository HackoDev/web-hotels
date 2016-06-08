from apps.admin.views import (
    CountryAdminListView, CountryAddChangeView, CityAdminListView, CityAddChangeView, HotelAddChangeView,
    HotelAdminListView, CountryDeleteView, CityDeleteView, HotelDeleteView, RoomPriceAddChangeView,
    RoomAdminListView, RoomAddChangeView, RoomDeleteView, IndexView, RoomPriceAdminListView, RoomPriceDeleteView,
    UserAddChangeView, UserDeleteView, UserAdminListView, ReservationAdminListView, ReservationAddChangeView,
    ReservationAddChangeView, ReservationDeleteView
)
from tornado.web import url

url_patterns = [
    url(r'^/admin/$', IndexView, name='admin:index'),
    url(r'^/admin/countries/$', CountryAdminListView, name='admin:country-list'),
    url(r'/admin/cities/', CityAdminListView, name='admin:city-list'),
    url(r'/admin/hotels/', HotelAdminListView, name='admin:hotel-list'),
    url(r'/admin/rooms/', RoomAdminListView, name='admin:room-list'),
    url(r'/admin/room-prices/', RoomPriceAdminListView, name='admin:room-price-list'),
    url(r'/admin/user/', UserAdminListView, name='admin:user-list'),
    url(r'/admin/reservation/', ReservationAdminListView, name='admin:reservation-list'),


    url(r'/admin/countries/add/', CountryAddChangeView, name='admin:country-add'),
    url(r'/admin/city/add/', CityAddChangeView, name='admin:city-add'),
    url(r'/admin/hotel/add/', HotelAddChangeView, name='admin:hotel-add'),
    url(r'/admin/room/add/', RoomAddChangeView, name='admin:room-add'),
    url(r'/admin/room-price/add/', RoomPriceAddChangeView, name='admin:room-price-add'),
    url(r'/admin/user/add/', UserAddChangeView, name='admin:user-add'),
    url(r'/admin/reservation/add/', ReservationAddChangeView, name='admin:reservation-add'),

    url(r'^/admin/countries/(?P<pk>\d+)/$', CountryAddChangeView, name='admin:country-change'),
    url(r'^/admin/city/(?P<pk>\d+)/$', CityAddChangeView, name='admin:city-change'),
    url(r'^/admin/hotel/(?P<pk>\d+)/$', HotelAddChangeView, name='admin:hotel-change'),
    url(r'^/admin/room/(?P<pk>\d+)/$', RoomAddChangeView, name='admin:room-change'),
    url(r'^/admin/room-price/(?P<pk>\d+)/$', RoomPriceAddChangeView, name='admin:room-price-change'),
    url(r'^/admin/user/(?P<pk>\d+)/$', UserAddChangeView, name='admin:user-change'),
    url(r'^/admin/reservation/(?P<pk>\d+)/$', ReservationAddChangeView, name='admin:reservation-change'),
    # delete urls
    url(r'/admin/countries/(?P<pk>\d+)/delete/', CountryDeleteView, name='admin:country-delete'),
    url(r'/admin/city/(?P<pk>\d+)/delete/', CityDeleteView, name='admin:city-delete'),
    url(r'/admin/hotel/(?P<pk>\d+)/delete/', HotelDeleteView, name='admin:hotel-delete'),
    url(r'/admin/room/(?P<pk>\d+)/delete/', RoomDeleteView, name='admin:room-delete'),
    url(r'/admin/room-price/(?P<pk>\d+)/delete/', RoomPriceDeleteView, name='admin:room-price-delete'),
    url(r'/admin/user/(?P<pk>\d+)/delete/', UserDeleteView, name='admin:user-delete'),
    url(r'/admin/reservation/(?P<pk>\d+)/delete/', ReservationDeleteView, name='admin:reservation-delete')
]
