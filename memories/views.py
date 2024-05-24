from django.shortcuts import render, redirect
from django.conf import settings
from .models import Memory


def index(request):
    user = request.user
    memories = None
    if user.is_authenticated:
        memories = Memory.objects.filter(user=user)
    return render(request, 'base.html', {'memories': memories})
