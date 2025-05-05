# Импортируем модель AbstractUser из django.contrib.auth.models
from django.contrib.auth.models import AbstractUser
# Импортируем модель Model из django.db
from django.db import models

# Определяем модель Role, которая представляет роль пользователя (Поставщик или Покупатель)
class Role(models.Model):
    # Определяем выборку ролей (Поставщик или Покупатель)
    ROLE_CHOICES = [
        ("Supplier", "Поставщик"),
        ("Customer", "Покупатель"),
    ]

    # Поле role, которое хранит название роли
    role = models.CharField(
        max_length=100, unique=True, db_index=True, choices=ROLE_CHOICES
    )

    # Метод __str__ для представления объекта Role в виде строки
    def __str__(self):
        return self.role

# Определяем модель ApiUser, которая расширяет модель AbstractUser
class ApiUser(AbstractUser):
    # Поле role, которое связывает пользователя с его ролью (моделью Role)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )

# Определяем модель Warehouse, которая представляет склад
class Warehouse(models.Model):
    # Поле name, которое хранит название склада
    name = models.CharField(max_length=60)
    # Поле user, которое связывает склад с пользователем (моделью ApiUser)
    user = models.ForeignKey(ApiUser, on_delete=models.CASCADE)

# Определяем модель Products, которая представляет продукт
class Products(models.Model):
    # Поле product, которое хранит название продукта
    product = models.CharField(max_length=255)
    # Поле price, которое хранит цену продукта
    price = models.PositiveIntegerField()
    # Поле count, которое хранит количество продукта по умолчанию (1)
    count = models.PositiveIntegerField(default=1)
    # Поле warehouses, которое связывает продукт со складом (моделью Warehouse)
    warehouses = models.ForeignKey(Warehouse, on_delete=models.CASCADE)