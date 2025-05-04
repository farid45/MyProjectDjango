

from rest_framework import serializers


from .models import ApiUser, Role, Products, Warehouse



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role']




class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    class Meta:
        model = ApiUser
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True, 'required': True, 'style': {'input_type': 'password'}}}


    def create(self, validated_data):
        role_data = validated_data.pop('role')
        role, _ = Role.objects.get_or_create(role=role_data['role'])
        user = ApiUser.objects.create(**validated_data, role=role)
        user.set_password(validated_data['password'])
        user.save(update_fields=["password"])
        return user

    def update(self, instance, validated_data):
        role_data = validated_data.pop('role', None)
        if role_data:
            role = Role.objects.get_or_create(name=role_data['role'])
            instance.role = role

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save(update_fields=["password"])
        else:
            instance.save()
        return instance


class WarehouseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'product', 'price', 'count', 'warehouses']
        extra_kwargs = {"id": {"read_only": True}, "count": {"read_only": True}}

    def create(self, validated_data):
        product = Products.objects.filter(product=validated_data['product'], price=validated_data['price']).first()

        if product:
            product.count += 1
            product.save(update_fields=['count'])
            return product
        else:
            validated_data['count'] = 1
            return super().create(validated_data)


class DelSerializer(serializers.ModelSerializer):
        class Meta:
            model = Products
            fields = ['id', 'product', 'price', 'count', 'warehouses']
            extra_kwargs = {"id": {"read_only": True}, "count": {"read_only": True}}

        def create(self, validated_data):
            product = Products.objects.filter(product=validated_data['product'], price=validated_data['price']).first()

            if product:
                product.count -= 1
                product.save(update_fields=['count'])
                if product.count == 0:
                    product.delete()
                return product
            else:
                validated_data['count'] = 0
                instance = super().create(validated_data)
                if instance.count == 0:
                    instance.delete()
                    raise serializers.ValidationError(f"Продукт '{instance.product}' по цене {instance.price} Продан.")
                return instance