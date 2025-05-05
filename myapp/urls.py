from rest_framework.routers import DefaultRouter

from .views import (
    DelModelViewSet,
    ProductsModelViewSet,
    UserModelViewSet,
    WarehouseModelViewSet,
)

router = DefaultRouter()
router.register("users", UserModelViewSet)
router.register("warehouses", WarehouseModelViewSet)
router.register(r"products", ProductsModelViewSet, basename="products")
router.register(r"del", DelModelViewSet, basename="del")
urlpatterns = []

urlpatterns.extend(router.urls)
