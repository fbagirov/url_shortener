from django import forms

from shortenedurl.models import URL
from django.core.exceptions import ValidationError


class URLCreateForm(forms.ModelForm):
    class Meta:
        model = URL
        exclude = ('hits', 'created_at')
        widgets = {'created_by': forms.HiddenInput()}

    full_url = forms.CharField(
        widget=forms.URLInput(
            attrs={'class': 'form-control', 'placeholder': 'Add Full URL'}
        )
    )

    shortened_url = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Add Custom URL (8 characters long)'}
        )
    )

#    def cleaned_shortened_url(self):
#    	data = self.clean()
#    	shortened_url = data.get("shortened_url")
#    	if len(shortened_url) < 8:
#    		raise ValidationError({
#    			'shortened_url': 'The shortened URL should be at least 8 characters long'
#    			})
#        elif len(shortened_url) > 8:
#        	raise ValidationError({
#        		'shortened_url': 'The shortened URL should be no more 8 characters long'
#        		})
