from django.db import transaction
from rest_framework import serializers

from shop import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderProduct
        fields = ("product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, write_only=True)

    class Meta:
        model = models.Order
        fields = ("id", "total_amount", "status", "products", "time_created")
        read_only_fields = ("id", "total_amount", "status", "time_created", "time_accepted")

    def create(self, validated_data):
        products_data = validated_data.pop("products")

        with transaction.atomic():
            order = models.Order()
            order_products, db_products, total_amount = [], [], 0

            for product_data in products_data:
                db_product = product_data["product"]
                db_product.available_quantity -= product_data["quantity"]
                quantity = product_data["quantity"]
                order_products.append(models.OrderProduct(order=order, product=db_product, quantity=quantity))
                db_products.append(db_product)
                total_amount += db_product.price * quantity
            order.total_amount = total_amount
            order.save()
            models.OrderProduct.objects.bulk_create(order_products)
            models.Product.objects.bulk_update(db_products, ["available_quantity"])
            return order

    def validate_products(self, products):
        for product in products:
            db_product = product["product"]
            if product["quantity"] > db_product.available_quantity:
                raise serializers.ValidationError(
                    f"Товара {db_product.name} нет в наличии. На складе осталось {db_product.available_quantity}"
                )
        return products


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = "__all__"
        read_only_fields = ("id", "total_amount", "status")
