from django import forms
from .models import Memory


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        exclude = ['user', 'slug']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
        error_messages = {
            'latitude': {
                'required': 'Укажите место на карте: неизвестная широта',
            },
            'longitude': {
                'required': 'Укажите место на карте: неизвестная долгота',
            },
        }
