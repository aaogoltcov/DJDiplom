from django.contrib.auth.models import User
from django.db import models

from cart.models import Cart


class Order(models.Model):  # Заказ
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    goods_count = models.IntegerField(verbose_name='Количество товаров', null=True)
    goods_price = models.IntegerField(verbose_name='Цена товаров', null=True)
    cart = models.ManyToManyField(Cart, verbose_name='Корзина')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return '%s %s' % (self.user, self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
