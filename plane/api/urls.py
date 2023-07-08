from django.urls import path, include
from plane.api.views import TicketAPIView, PlaneAPIView

urlpatterns = [
    path('planes/', PlaneAPIView.as_view(), name="plane_api"),
    path('planes/<int:pk>/', PlaneAPIView.as_view(), name="plane_api_detail"),
    path('planes/ticket/', TicketAPIView.as_view(), name='ticket_api'),
    path('planes/ticket/<int:pk>/', TicketAPIView.as_view(), name='ticket_api_detail')
]
