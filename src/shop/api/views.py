from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from core.settings import DJANGO_CACHE_TIME
from shop import models
from shop.api import mixins, serializers


class ProductViewSet(mixins.RetriveListModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    @method_decorator(cache_page(DJANGO_CACHE_TIME))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OrderViewSet(mixins.CreateModelViewSet):
    queryset = models.Order.objects.prefetch_related(
        Prefetch("products", to_attr="products", queryset=models.OrderProduct.objects.select_related("product"))
    ).all()
    serializer_class = serializers.OrderSerializer


class PaymentViewSet(mixins.CreateModelViewSet):
    queryset = models.Payment.objects.select_related("order").all()
    serializer_class = serializers.PaymentSerializer
