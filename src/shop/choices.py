from django.db import models


class OrderStatusChoices(models.TextChoices):
    PENDING = "pending", "На рассмотрении"
    ACCEPTED = "accepted", "Подтверждён"
    REJECTED = "rejected", "Отклонён"


class PaymentStatusChoices(models.TextChoices):
    PENDING = "pending", "В процессе оплаты"
    ACCEPTED = "accepted", "Оплачено"
    REJECTED = "rejected", "Не оплачено"


class PaymentTypeChoices(models.TextChoices):
    PIN = "pin", "Оплата картой"
    CASH = "cash", "Оплата наличными"
