from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, CustomTokenObtainPairView, YandexOAuth2View

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # dj-rest-auth базовые (login/logout/password)
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/yandex/', YandexOAuth2View.as_view(), name='yandex_login'),
]

