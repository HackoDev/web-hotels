from .views import HotelSearchListView, RoomSearchListView, HotelDetailsView

url_patterns = [
    (r'/api/v1/hotels/', HotelSearchListView),
    (r'/api/v1/hotels/(?P<hotel_id>\d+)/', HotelDetailsView),
    (r'/api/v1/rooms/', RoomSearchListView)
]