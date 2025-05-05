# Импортируем модуль permissions из rest_framework
from rest_framework import permissions

# Определяем класс IsSupplierOrReadOnly, который наследовался от BasePermission
class IsSupplierOrReadOnly(permissions.BasePermission):
    # Метод has_permission проверяет, имеет ли пользователь разрешение на выполнение запроса
    def has_permission(self, request, view):
        # Проверяем, аутентифицирован ли пользователь
        if request.user and request.user.is_authenticated:
            # Получаем роль пользователя
            user_role = request.user.role.role if request.user.role else None
            # Если роль пользователя "Поставщик", возвращаем True (разрешаем доступ)
            if user_role == "Supplier":
                return True
            # Если метод запроса безопасный (GET, HEAD или OPTIONS), возвращаем True (разрешаем доступ)
            elif request.method in permissions.SAFE_METHODS:
                return True
        # Если пользователь не аутентифицирован или не является персоналом, возвращаем False (отказываем доступ)
        return bool(request.user and request.user.is_staff)

# Определяем класс IsCustomerOrReadOnly, который наследовался от BasePermission
class IsCustomerOrReadOnly(permissions.BasePermission):
    # Метод has_permission проверяет, имеет ли пользователь разрешение на выполнение запроса
    def has_permission(self, request, view):
        # Проверяем, аутентифицирован ли пользователь
        if request.user and request.user.is_authenticated:
            # Получаем роль пользователя
            user_role = request.user.role.role if request.user.role else None
            # Если роль пользователя "Покупатель", возвращаем True (разрешаем доступ)
            if user_role == "Customer":
                return True
            # Если метод запроса безопасный (GET, HEAD или OPTIONS), возвращаем True (разрешаем доступ)
            elif request.method in permissions.SAFE_METHODS:
                return True
        # Если пользователь не аутентифицирован или не является персоналом, возвращаем False (отказываем доступ)
        return bool(request.user and request.user.is_staff)