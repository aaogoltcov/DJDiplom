from django.contrib.auth.models import User
from django.db import models

from shop.models import Good


class Cart(models.Model):  # Корзина, товары отсюда не удаляются, в случае, если товар был заказан, у него меняется
    # статус is_ordered на True, при это в корзине всегда отображаются товары с is_ordered, который False -
    # это сделано специально, чтобы можно отследить какие товары пользователь добавлял в корзину и построить аналитику
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='Продукт', null=True)
    is_ordered = models.BooleanField(verbose_name='Признак заказа', null=False, default=False)

    def __str__(self):
        return '%s' % (self.good,)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
