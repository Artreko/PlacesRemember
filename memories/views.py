from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.conf import settings
from .models import Memory
from .forms import MemoryForm


def home(request):
    user = request.user
    memories = None
    if user.is_authenticated:
        memories = Memory.objects.filter(user=user)
    return render(request, 'home.html', {'memories': memories})


class MemoryCreateView(LoginRequiredMixin, CreateView):
    form_class = MemoryForm
    model = Memory
    template_name = 'memories/memory_create.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
