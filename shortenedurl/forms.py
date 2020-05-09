import requests
from django import forms
from django.core.exceptions import ValidationError

from shortenedurl.models import URL


class URLCreateForm(forms.ModelForm):
    class Meta:
        model = URL
        exclude = ('hits', 'shortened_url', 'created_at')
        widgets = {
            'full_url': forms.Textarea(attrs={'class': 'form-control'})
        }
