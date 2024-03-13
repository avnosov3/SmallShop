from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from shop.api import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("products", views.ProductViewSet, basename="products")
router.register("orders", views.OrderViewSet, basename="orders")
router.register("payments", views.PaymentViewSet, basename="payments")

app_name = "api"
urlpatterns = router.urls
