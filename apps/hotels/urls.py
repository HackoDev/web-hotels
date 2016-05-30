from .views import HotelSearchListView, RoomSearchListView

url_patterns = [
    (r'/hotels/', HotelSearchListView),
    (r'/rooms/', RoomSearchListView)
]