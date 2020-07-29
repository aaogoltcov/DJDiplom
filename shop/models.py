from django.contrib.auth.models import User
from django.db import models


class Paper(models.Model):  # Моделя по огранизации статей на главной странице, и товаров, которые привязаны к ним
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


class Catalog(models.Model):  # Общий каталог для всех товаров
    name = models.CharField(verbose_name='Название каталога', max_length=40)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    order = models.IntegerField(verbose_name='Порядок')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'


class SubCatalog(models.Model):  # Общий подкаталог для всех товаров
    name = models.CharField(verbose_name='Название каталога', max_length=40)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    order = models.IntegerField(verbose_name='Порядок')
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкаталог'
        verbose_name_plural = 'Подкаталоги'


class Good(models.Model):  # Модель, которая описывает сам товар
    name = models.CharField(verbose_name='Название товара', max_length=60)
    image = models.FilePathField(verbose_name='Фотография телефона', path='static')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField(verbose_name='Описание', max_length=200, null=True, blank=True)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, null=True)
    sub_catalog = models.ForeignKey(SubCatalog, on_delete=models.CASCADE, null=True, blank=True)
    papers = models.ForeignKey(Paper, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена товара', null=True)

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


class Feedback(models.Model):  # Модель, которая хранит в себе отзывы по товарам в модели Good
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='Продукт', null=True)
    person_name = models.CharField(verbose_name='Имя автора', max_length=40, null=True)
    score = models.CharField(verbose_name='Оценка', null=True, choices=SCORE_CHOICES, max_length=10)
    description = models.TextField(verbose_name='Отзыв', max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    # csrftoken хранится для распознования анонимных пользователей
    csrftoken = models.CharField(verbose_name='CSRFTOKEN', null=True, blank=True, max_length=200)

    def __str__(self):
        return self.person_name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'