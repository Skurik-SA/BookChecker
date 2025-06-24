import requests
from allauth.socialaccount.providers.oauth2.client import OAuth2Client as BaseOAuth2Client
from allauth.socialaccount.providers.yandex.views import YandexOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Регистрация прошла успешно'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class YandexOAuth2View(APIView):
    """
    Обменивает code → access_token у Яндекса, получает инфо о пользователе,
    создаёт/находит User и возвращает JWT-токены.
    """
    authentication_classes = []  # публичный
    permission_classes     = []  # публичный

    def post(self, request):
        code = request.data.get('code')
        redirect_uri = request.data.get('redirect_uri')
        if not code or not redirect_uri:
            return Response(
                {'detail': 'Параметры code и redirect_uri обязательны.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1) Обмениваем code → access_token
        token_resp = requests.post(
            'https://oauth.yandex.ru/token',
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'client_id':     settings.SOCIALACCOUNT_PROVIDERS['yandex']['APP']['client_id'],
                'client_secret': settings.SOCIALACCOUNT_PROVIDERS['yandex']['APP']['secret'],
                'redirect_uri': redirect_uri,
            },
            timeout=5
        )

        if token_resp.status_code != 200:
            return Response(
                {'detail': 'Ошибка обмена кода на токен', 'info': token_resp.json()},
                status=token_resp.status_code
            )
        token_data = token_resp.json()
        access_token = token_data.get('access_token')

        # 2) Получаем данные пользователя
        info_resp = requests.get(
            'https://login.yandex.ru/info',
            params={'format': 'json'},
            headers={'Authorization': f'OAuth {access_token}'},
            timeout=5
        )
        if info_resp.status_code != 200:
            return Response(
                {'detail': 'Ошибка получения информации о пользователе', 'info': info_resp.json()},
                status=info_resp.status_code
            )
        info = info_resp.json()
        # Яндекс возвращает default_email и id
        email = info.get('default_email')
        username = info.get('login') or info.get('id')

        if not email:
            return Response(
                {'detail': 'У этого аккаунта нет публичной почты в Яндексе.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3) Создаём или получаем пользователя
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        # 4) Генерируем JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access':  str(refresh.access_token),
            'user': {
                'pk':      user.pk,
                'username':user.username,
                'email':   user.email,
            }
        })
