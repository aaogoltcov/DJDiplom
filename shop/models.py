from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db import models


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class Paper(models.Model):
    name = models.CharField(verbose_name='Название статьи', max_length=40)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(verbose_name='Заголовок статьи', max_length=40)
    text = models.TextField(verbose_name='Текст статьи', max_length=200)
    order = models.IntegerField(verbose_name='Порядок')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Catalog(models.Model):
    name = models.CharField(verbose_name='Название каталога', max_length=40)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    order = models.IntegerField(verbose_name='Порядок')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'


class SubCatalog(models.Model):
    name = models.CharField(verbose_name='Название каталога', max_length=40)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    order = models.IntegerField(verbose_name='Порядок')
    catalogs = models.ForeignKey(Catalog, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкаталог'
        verbose_name_plural = 'Подкаталоги'


class Good(models.Model):
    name = models.CharField(verbose_name='Название телефона', max_length=60)
    image = models.FilePathField(verbose_name='Фотография телефона', path='static')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField(verbose_name='Описание', max_length=200, null=True, blank=True)
    catalogs = models.ForeignKey(Catalog, on_delete=models.CASCADE, null=True)
    sub_catalogs = models.ForeignKey(SubCatalog, on_delete=models.CASCADE, null=True, blank=True)
    papers = models.ForeignKey(Paper, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


SCORE_CHOICES = [
    ('★★★★★', '★★★★★'),
    ('★★★★', '★★★★'),
    ('★★★', '★★★'),
    ('★★', '★★'),
    ('★', '★'),
]


class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='Продукт', null=True)
    person_name = models.CharField(verbose_name='Имя автора', max_length=40, null=True)
    score = models.CharField(verbose_name='Оценка', null=True, choices=SCORE_CHOICES, max_length=10)
    description = models.TextField(verbose_name='Отзыв', max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    csrftoken = models.CharField(verbose_name='CSRFTOKEN', null=True, blank=True, max_length=200)

    def __str__(self):
        return self.person_name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='Продукт', null=True)
    is_ordered = models.BooleanField(verbose_name='Признак заказа', null=False, default=False)

    def __str__(self):
        return '%s' % (self.good, )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    goods_count = models.IntegerField(verbose_name='Количество товаров', null=True)
    cart = models.ManyToManyField(Cart, verbose_name='Корзина')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return '%s %s' % (self.user, self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
