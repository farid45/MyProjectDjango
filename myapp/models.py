from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    ROLE_CHOICES = [
        ('Supplier', 'Поставщик'),
        ('Customer', 'Покупатель'),
    ]

    role = models.CharField(max_length=100, unique=True, db_index=True, choices=ROLE_CHOICES)

    def __str__(self):
        return self.role


class ApiUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')





class Warehouse(models.Model):
    name = models.CharField(max_length=60)
    user = models.ForeignKey(ApiUser, on_delete=models.CASCADE)

class Products(models.Model):
    product = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=1)
    warehouses = models.ForeignKey(Warehouse, on_delete=models.CASCADE)








