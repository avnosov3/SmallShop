import logging

from celery import shared_task

from core.settings import CELERY_RETRY_ATTEMPTS, CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS
from shop.http_client import order_client

logger = logging.getLogger(__name__)


@shared_task(bind=True, default_retry_delay=CELERY_RETRY_ATTEMPTS)
def post_order(self, data: dict):
    try:
        response = order_client.post_order(data)
        print(response)
    except Exception as error:
        logger.exception(error)
        raise self.retry(exc=error, countdown=CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS)
    return "Заказ успешно отправлен"
