from django.core.validators import MinValueValidator, validate_image_file_extension
from django.db import models

from shop.choices import OrderStatusChoices, PaymentStatusChoices, PaymentTypeChoices


class Product(models.Model):
    name = models.CharField(verbose_name="Название товара", max_length=200, unique=True)
    price = models.DecimalField(
        verbose_name="Цена товара",
        max_digits=19,
        decimal_places=2,
        validators=[MinValueValidator(0, message="Цена товара не может быть отрицательной")],
    )
    content = models.TextField(verbose_name="Описание товара", blank=True, null=True)
    available_quantity = models.PositiveIntegerField(verbose_name="Доступное количество")
    image = models.ImageField(
        verbose_name="Изображение товара",
        upload_to="shop/images/",
        blank=True,
        null=True,
        validators=[validate_image_file_extension],
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"Товар: {self.name[:15]}, цена: {self.price}"


class Order(models.Model):
    total_amount = models.DecimalField(
        verbose_name="Итоговая сумма",
        max_digits=19,
        decimal_places=2,
        validators=[MinValueValidator(0, message="Цена товара не может быть отрицательной")],
        default=0,
    )
    status = models.CharField(
        verbose_name="Статус заказа",
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
    )
    time_created = models.DateTimeField(verbose_name="Время создания заказа", auto_now_add=True)
    time_accepted = models.DateTimeField(verbose_name="Время подтверждения заказа", auto_now=True)
    products = models.ManyToManyField(
        verbose_name="Товары", to=Product, through="OrderProduct", blank=True, related_name="orders"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ: {self.pk}, статус: {self.status}, итоговая сумма: {self.total_amount}"


class Payment(models.Model):
    order = models.OneToOneField(
        verbose_name="Заказ",
        to=Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )
    total_amount = models.DecimalField(
        verbose_name="Итоговая сумма",
        max_digits=19,
        decimal_places=2,
        validators=[MinValueValidator(0, message="Цена товара не может быть отрицательной")],
        default=0,
    )
    status = models.CharField(
        verbose_name="Статус оплаты",
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
    )
    type = models.CharField(
        verbose_name="Тип оплаты",
        choices=PaymentTypeChoices.choices,
        default=PaymentTypeChoices.PIN,
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"Оплата: {self.pk}, статус: {self.status}, тип: {self.type}"

    def save(self, *args, **kwargs):
        if self.order:
            self.total_amount = self.order.total_amount
        super().save(*args, **kwargs)


class OrderProduct(models.Model):
    order = models.ForeignKey(verbose_name="Заказ", to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(verbose_name="Товар", to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество товаров")

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def __str__(self):
        return f"Товар: {self.product}, количество: {self.quantity}"
