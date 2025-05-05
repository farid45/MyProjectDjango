# Импортируем модуль serializers из rest_framework
from rest_framework import serializers

# Импортируем модели ApiUser, Products, Role и Warehouse из текущего приложения
from .models import ApiUser, Products, Role, Warehouse

# Определяем сериализатор для модели Role
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        # Указываем модель, с которой будет работать сериализатор
        model = Role
        # Указываем поля, которые будут сериализованы
        fields = ["role"]

# Определяем сериализатор для модели ApiUser
class UserSerializer(serializers.ModelSerializer):
    # Встраиваем сериализатор Role в сериализатор ApiUser
    role = RoleSerializer()

    class Meta:
        # Указываем модель, с которой будет работать сериализатор
        model = ApiUser
        # Указываем поля, которые будут сериализованы
        fields = ["id", "username", "email", "password", "role"]
        # Дополнительные параметры для полей
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {
                "write_only": True,
                "required": True,
                "style": {"input_type": "password"},
            },
        }

    # Метод create создает новый экземпляр модели ApiUser с валидированными данными
    def create(self, validated_data):
        # Извлекаем данные роли из валидированных данных
        role_data = validated_data.pop("role")
        # Получаем или создаем роль по имени
        role, _ = Role.objects.get_or_create(role=role_data["role"])
        # Создаем нового пользователя с валидированными данными и назначенной ролью
        user = ApiUser.objects.create(**validated_data, role=role)
        # Устанавливаем пароль для пользователя и сохраняем его
        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        # Возвращаем созданного пользователя
        return user

    # Метод update обновляет существующий экземпляр модели ApiUser валидированными данными
    def update(self, instance, validated_data):
        # Извлекаем данные роли из валидированных данных (если они есть)
        role_data = validated_data.pop("role", None)
        # Если данные роли присутствуют, получаем или создаем роль по имени и назначаем ее пользователю
        if role_data:
            role = Role.objects.get_or_create(name=role_data["role"])
            instance.role = role

        # Если пароль присутствует в валидированных данных, устанавливаем его и сохраняем пользователя
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            instance.save(update_fields=["password"])
        # В противном случае просто сохраняем пользователя
        else:
            instance.save()
        # Возвращаем обновленного пользователя
        return instance

# Определяем сериализатор для модели Warehouse
class WarehouseSerializers(serializers.ModelSerializer):
    class Meta:
        # Указываем модель, с которой будет работать сериализатор
        model = Warehouse
        # Указываем поля, которые будут сериализованы (все поля модели)
        fields = "__all__"
        # Дополнительные параметры для полей
        extra_kwargs = {"id": {"read_only": True}}

# Определяем сериализатор для модели Products
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        # Указываем модель, с которой будет работать сериализатор
        model = Products
        # Указываем поля, которые будут сериализованы
        fields = ["id", "product", "price", "count", "warehouses"]
        # Дополнительные параметры для полей
        extra_kwargs = {"id": {"read_only": True}, "count": {"read_only": True}}

    # Метод create создает новый экземпляр модели Products с валидированными данными
    def create(self, validated_data):
        # Пытаемся найти продукт с таким же именем и ценой в базе данных
        product = Products.objects.filter(
            product=validated_data["product"], price=validated_data["price"]
        ).first()

        # Если продукт уже exists, увеличиваем его количество на 1
        if product:
            product.count += 1
            product.save(update_fields=["count"])
            return product
        # В противном случае создаем новый продукт с количеством 1
        else:
            validated_data["count"] = 1
            return super().create(validated_data)

# Определяем сериализатор для модели Products с методом create для уменьшения количества товара
class DelSerializer(serializers.ModelSerializer):
    class Meta:
        # Указываем модель, с которой будет работать сериализатор
        model = Products
        # Указываем поля, которые будут сериализованы
        fields = ["id", "product", "price", "count", "warehouses"]
        # Дополнительные параметры для полей
        extra_kwargs = {"id": {"read_only": True}, "count": {"read_only": True}}

    # Метод create создает новый экземпляр модели Products с валидированными данными или уменьшает количество товара
    def create(self, validated_data):
        # Пытаемся найти продукт с таким же именем и ценой в базе данных
        product = Products.objects.filter(
            product=validated_data["product"], price=validated_data["price"]
        ).first()

        # Если продукт уже exists, уменьшаем его количество на 1
        if product:
            product.count -= 1
            product.save(update_fields=["count"])
            # Если количество товара стало равно 0, удаляем продукт
            if product.count == 0:
                product.delete()
            return product
        # В противном случае создаем новый продукт с количеством 0 и генерируем ошибку валидации
        else:
            validated_data["count"] = 0
            instance = super().create(validated_data)
            if instance.count == 0:
                instance.delete()
                raise serializers.ValidationError(
                    f"Продукт '{instance.product}' " f"по цене {instance.price} Продан."
                )
            return instance