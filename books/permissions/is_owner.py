from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Разрешает изменять/удалять объект только его владельцу.
    Чтение — всем, если не переопределено другим пермишном.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS — GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # сначала пробуем взять прямое поле .user
        owner = getattr(obj, 'user', None)
        if owner is not None:
            return owner == request.user

        # если нет, может быть вложенный объект Note: смотрим entry.user
        entry = getattr(obj, 'entry', None)
        if entry is not None:
            return entry.user == request.user

        # по-умолчанию отказываем
        return False