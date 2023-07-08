from django.urls import path, include

urlpatterns = [
    path('api/', include('hotel.api.urls'))
]