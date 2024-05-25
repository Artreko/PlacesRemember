from django.urls import path, include
from .views import home, MemoryCreateView, MemoryUpdateView

memory_urlpatterns = [
    path('create', MemoryCreateView.as_view(), name='create-memory'),
    path('edit/<str:slug>', MemoryUpdateView.as_view(), name='edit-memory')
]

urlpatterns = [
    path('memory/', include(memory_urlpatterns)),
    path('', home, name='home'),
]
