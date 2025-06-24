from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Диктуем SimpleJWT: поле для входа в запросе — 'username'
    username_field = 'username'

    def validate(self, attrs):
        identifier = attrs.get("username")
        password   = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError(_("Логин (username/email) и пароль обязательны"))

        # Ищем user по username или по email
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                raise serializers.ValidationError(_("Пользователь не найден"))

        if not user.check_password(password):
            raise serializers.ValidationError(_("Неверный пароль"))
        if not user.is_active:
            raise serializers.ValidationError(_("Пользователь заблокирован"))

        # Генерируем токены
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access':  str(refresh.access_token),
        }
        # При желании — доп. поля
        data['user_id']  = user.id
        data['username'] = user.username
        return data