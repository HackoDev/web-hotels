from .views import HotelSearchListView, RoomSearchListView, HotelDetailsView, ReservationSetView, CountriesListView, \
    CitiesListView

url_patterns = [
    (r'^/api/v1/hotels/$', HotelSearchListView),
    (r'^/api/v1/hotels/(?P<hotel_id>\d+)/$', HotelDetailsView),
    (r'^/api/v1/rooms/(?P<room_id>\d+)/$', ReservationSetView),
    (r'^/api/v1/rooms/$', RoomSearchListView),
    (r'^/api/v1/countries/$', CountriesListView),
    (r'^/api/v1/cities/$', CitiesListView)
]