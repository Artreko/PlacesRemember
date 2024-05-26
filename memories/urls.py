from django.urls import path, include
from .views import home, MemoryCreateView, MemoryUpdateView

memory_urlpatterns = [
    path('create', MemoryCreateView.as_view(), name='memory-create'),
    path('edit/<str:slug>', MemoryUpdateView.as_view(), name='memory-edit')
]

urlpatterns = [
    path('memory/', include(memory_urlpatterns)),
    path('', home, name='home'),
]
