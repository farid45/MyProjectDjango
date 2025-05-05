# Импортируем viewsets из rest_framework
from rest_framework import viewsets

# Импортируем модели ApiUser, Products и Warehouse из текущего приложения
from .models import ApiUser, Products, Warehouse

# Импортируем классы разрешений IsCustomerOrReadOnly и IsSupplierOrReadOnly из модуля permisions текущего приложения
from .permisions import IsCustomerOrReadOnly, IsSupplierOrReadOnly

# Импортируем сериализаторы UserSerializer, ProductsSerializer, WarehouseSerializers и DelSerializer из модуля serializers текущего приложения
from .serializers import (
    DelSerializer,
    ProductsSerializer,
    UserSerializer,
    WarehouseSerializers,
)

# Определяем представление UserModelViewSet, которое наследуется от ModelViewSet
class UserModelViewSet(viewsets.ModelViewSet):
    # Указываем queryset, который будет использоваться для получения объектов модели ApiUser
    queryset = ApiUser.objects.all()
    # Указываем методы HTTP, которые будут разрешены для этого представления (только POST и GET)
    http_method_names = ["post", "get"]
    # Указываем сериализатор, который будет использоваться для сериализации и десериализации данных
    serializer_class = UserSerializer

    # Указываем аутентификационные классы, которые будут использоваться для аутентификации пользователей (по умолчанию None)
    authentication_classes = ()
    # Указываем классы разрешений, которые будут использоваться для проверки разрешений пользователей (по умолчанию None)
    permission_classes = ()

# Определяем представление WarehouseModelViewSet, которое наследуется от ModelViewSet
class WarehouseModelViewSet(viewsets.ModelViewSet):
    # Указываем queryset, который будет использоваться для получения объектов модели Warehouse
    queryset = Warehouse.objects.all()
    # Указываем сериализатор, который будет использоваться для сериализации и десериализации данных
    serializer_class = WarehouseSerializers
    # Указываем класс разрешений, который будет использоваться для проверки разрешений пользователей (только поставщики)
    permission_classes = (IsSupplierOrReadOnly,)

# Определяем представление ProductsModelViewSet, которое наследуется от ModelViewSet
class ProductsModelViewSet(viewsets.ModelViewSet):
    # Указываем queryset, который будет использоваться для получения объектов модели Products
    queryset = Products.objects.all()
    # Указываем сериализатор, который будет использоваться для сериализации и десериализации данных
    serializer_class = ProductsSerializer
    # Указываем класс разрешений, который будет использоваться для проверки разрешений пользователей (только поставщики)
    permission_classes = (IsSupplierOrReadOnly,)

# Определяем представление DelModelViewSet, которое наследуется от ModelViewSet
class DelModelViewSet(viewsets.ModelViewSet):
    # Указываем queryset, который будет использоваться для получения объектов модели Products
    queryset = Products.objects.all()
    # Указываем сериализатор, который будет использоваться для сериализации и десериализации данных
    serializer_class = DelSerializer
    # Указываем класс разрешений, который будет использоваться для проверки разрешений пользователей (только покупатели)
    permission_classes = (IsCustomerOrReadOnly,)