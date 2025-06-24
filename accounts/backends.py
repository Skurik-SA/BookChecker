from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Позволяет аутентифицироваться по username **или** по email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 'username' здесь -- это то, что придёт с формы: либо логин, либо почта
        user = None
        if username is None or password is None:
            return None

        # Попробуем по username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Попробуем по email
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
