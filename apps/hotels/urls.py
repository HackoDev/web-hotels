from .views import HotelSearchListView

url_patterns = [
    (r'/hotels/', HotelSearchListView)
]