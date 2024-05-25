from django.urls import path, include
from .views import home, MemoryCreateView

memory_urlpatterns = [
    path('create', MemoryCreateView.as_view(), name='create-memory')
]

urlpatterns = [
    path('memory/', include(memory_urlpatterns)),
    path('', home, name='home'),
]
