from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import VkUser

admin.site.register(VkUser, UserAdmin)
