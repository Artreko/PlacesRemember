from django.db import models
from django.contrib.auth.models import AbstractUser


class VkUser(AbstractUser):
    vk_id = models.PositiveBigIntegerField('VK ID', db_index=True, unique=True)
    profile_image = models.URLField("Image URL")
    username = models.CharField("username", max_length=50, unique=False)
    USERNAME_FIELD = 'vk_id'
    REQUIRED_FIELDS = ['profile_image']
