import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from pytils.translit import slugify  

class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    slug = models.SlugField('Слаг', max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class City(models.Model):
    name = models.CharField('Город', max_length=100)

    def __str__(self):
        return self.name


class Ad(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads', verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    price = models.PositiveIntegerField('Цена (тенге)', help_text='0 — бесплатно')
    contact_phone = models.CharField('Телефон для связи', max_length=20, blank=True, default='')
    image_url = models.CharField('URL фото', max_length=500, blank=True, default='')
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    is_moderated = models.BooleanField('Прошло модерацию', default=False)
    is_top = models.BooleanField('Топ (VIP)', default=False)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'ad')

    def __str__(self):
        return f'{self.user.username} → {self.ad.title}'


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='written_reviews', verbose_name='Кто оставил')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews', verbose_name='Кому оставили')
    rating = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField('Комментарий', max_length=1000)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'reviewed_user')
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.reviewer.username} -> {self.reviewed_user.username} ({self.rating})'


class Banner(models.Model):
    name = models.CharField('Название компании', max_length=255, default='Company')
    image_url = models.CharField('URL фото', max_length=500)

    def __str__(self):
        return self.name