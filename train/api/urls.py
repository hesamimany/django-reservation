from django.urls import path, include
from train.api.views import TrainAPIView, TicketAPIView

urlpatterns = [
    path('trains/', TrainAPIView.as_view(), name="train_api"),
    path('trains/<int:pk>/', TrainAPIView.as_view(), name="train_api_detail"),
    path('trains/ticket/', TicketAPIView.as_view(), name='ticket_api'),
    path('trains/ticket/<int:pk>/', TicketAPIView.as_view(), name='ticket_api_detail')
]
