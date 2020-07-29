from django.contrib import admin

from cart.models import Cart
from orders.models import Order
from shop.models import Good, Feedback, Paper, Catalog, SubCatalog


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    pass


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCatalog)
class SubCatalogAdmin(admin.ModelAdmin):
    pass


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'good', 'is_ordered',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'goods_count', 'date',)
    search_fields = ('cart',)
    ordering = ('-date',)
