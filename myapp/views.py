
from rest_framework import viewsets

from .models import ApiUser, Warehouse, Products
from .permisions import IsCustomerOrReadOnly, IsSupplierOrReadOnly
from .serializers import UserSerializer, WarehouseSerializers, ProductsSerializer, DelSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = UserSerializer

    authentication_classes = []
    permission_classes = []


class WarehouseModelViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializers
    permission_classes = (IsSupplierOrReadOnly, )




class ProductsModelViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = (IsSupplierOrReadOnly,)

class DelModelViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = DelSerializer
    permission_classes = (IsCustomerOrReadOnly,)





