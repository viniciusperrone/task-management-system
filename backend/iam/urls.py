from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from iam.views import RegisterView, LoginView, UserListView, UserMeView


AUTH_PREFIX = "auth"

urlpatterns = [
    # Auth
    path(f'{AUTH_PREFIX}/register/', RegisterView.as_view(), name='auth_register'),
    path(f'{AUTH_PREFIX}/login/', LoginView.as_view(), name='auth_login'),
    path(f'{AUTH_PREFIX}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Users
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/me', UserMeView.as_view(), name='user_me'),
]
