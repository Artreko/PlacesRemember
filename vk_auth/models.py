from django.db import models
from django.contrib.auth.models import AbstractUser


class VkUser(AbstractUser):
    vk_id = models.PositiveBigIntegerField('VK ID', db_index=True, unique=True)
    profile_image = models.URLField("Image URL")
    REQUIRED_FIELDS = ['vk_id', 'profile_image']
