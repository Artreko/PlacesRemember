from django.db import models
from .utils import unique_slugify


class Memory(models.Model):
    user = models.ForeignKey(
        'vk_auth.VkUser', verbose_name='Пользователь', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=150)
    comment = models.TextField('Комментарий')
    latitude = models.DecimalField(
        'Широта', max_digits=27, decimal_places=23)
    longitude = models.DecimalField(
        'Долгота', max_digits=27, decimal_places=23)
    slug = models.SlugField('URL', unique=True)

    def save(self, **kwargs) -> None:
        unique_slugify(self, self.name)
        return super().save(**kwargs)
