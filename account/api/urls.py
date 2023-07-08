from django.urls import path
from account.api.views import UserAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('account/', UserAPIView.as_view(), name='user_api'),
    path('account/<int:pk>/', UserAPIView.as_view(), name='user_detail_api'),
    path('login/', LoginAPIView.as_view(), name='login_api'),
    path('logout/', LogoutAPIView.as_view(), name='logout_api'),
]