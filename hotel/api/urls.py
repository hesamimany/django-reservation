from django.urls import path, include
from hotel.api.views import HotelReservationAPIView, HotelAPIView

urlpatterns = [
    path('reservations/', HotelReservationAPIView.as_view(), name='hotel_reservation_api'),
    path('reservations/<int:pk>/', HotelReservationAPIView.as_view(), name='hotel_reservation_detail'),
    path('hotel/', HotelAPIView.as_view(), name='hotel_api'),
    path('hotel/<int:pk>/', HotelAPIView.as_view(), name='hotel_api_detail')
]
