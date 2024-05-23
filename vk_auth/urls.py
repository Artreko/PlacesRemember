from django.urls import path
from .views import auth_view, auth_code_view, logout_view

urlpatterns = [
    path('code/', auth_code_view, name='vk-auth-code'),
    path('', auth_view, name='vk-auth'),
    path('logout', logout_view, name='logout')
]
