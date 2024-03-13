from django.contrib import admin
from django.core.cache import caches
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django_object_actions import DjangoObjectActions, action

from core.settings import DEFAULT_CACHE
from shop import models
from shop.choices import OrderStatusChoices, PaymentStatusChoices
from shop.tasks import post_order


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"
    show_full_result_count = False
    list_select_related = True


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")


@admin.register(models.Product)
class ProductAdmin(DjangoObjectActions, BaseAdmin):
    list_display = ("id", "name", "price", "available_quantity")
    list_filter = ("available_quantity",)
    search_fields = ("name", "content")

    @action(label="Очистить кеш товаров")
    def clear_countries_cache(self, request, queryset):
        caches[DEFAULT_CACHE].clear()

    changelist_actions = ("clear_countries_cache",)


@admin.register(models.Order)
class OrderAdmin(BaseAdmin):
    list_display = ("id", "total_amount", "status", "time_created", "time_accepted")
    list_filter = ("status",)
    search_fields = ("pk", "products__name", "products__content")
    autocomplete_fields = ("products",)
    inlines = [OrderProductInline]

    CONFIRM_ORDER_BUTTON_TEXT = "confirm_order"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("payment").prefetch_related("products")

    def changeform_view(self, request, object_id, form_url, extra_context):
        extra_context = extra_context or {}
        extra_context["PAYMENT_STATUS"] = PaymentStatusChoices
        extra_context["CONFIRM_ORDER_BUTTON_TEXT"] = self.CONFIRM_ORDER_BUTTON_TEXT
        extra_context["ORDER_STATUS"] = OrderStatusChoices
        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        if self.CONFIRM_ORDER_BUTTON_TEXT in request.POST:
            self.handle_order_confirmation(obj)
            self.message_user(request, OrderStatusChoices.ACCEPTED.label)
        return super().response_change(request, obj)

    def handle_order_confirmation(self, order):
        order.status = OrderStatusChoices.ACCEPTED
        order.save()
        post_order.delay(
            {"id": order.id, "total_amount": str(order.total_amount), "time_accepted": str(order.time_accepted)}
        )


@admin.register(models.Payment)
class PaymentAdmin(BaseAdmin):
    list_display = ("id", "order", "status", "type", "total_amount")
    list_filter = ("status", "type")

    autocomplete_fields = ("order",)


@admin.register(models.OrderProduct)
class OrderProductAdmin(BaseAdmin):
    list_display = ("id", "order", "product", "quantity")
    list_filter = ("order",)
    search_fields = (
        "product__name",
        "product__content",
    )
    autocomplete_fields = ("order", "product")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("order", "product")
