from django import forms

from shortenedurl.models import URL


class URLCreateForm(forms.ModelForm):
    class Meta:
        model = URL
        exclude = ('hits', 'shortened_url', 'created_at')
        widgets = {'created_by': forms.HiddenInput()}

    full_url = forms.CharField(
        widget=forms.URLInput(
            attrs={'class': 'form-control', 'placeholder': 'Add Full URL'}
        )
    )
