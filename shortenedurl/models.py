from hashlib import md5

import requests
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models


class URL(models.Model):
    full_url = models.URLField(unique=True)
    shortened_url = models.URLField(unique=True)
    hits = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.hits += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.shortened_url = md5(self.full_url.encode()).hexdigest()[:10]

        return super().save(*args, **kwargs)

    def clean(self):
        validate = URLValidator()
        try:
            validate(self.full_url)
            requests.get(self.full_url)
        except ValidationError:
            raise ValidationError('Enter a valid URL')
        except requests.ConnectionError:
            raise ValidationError({
                'full_url': 'URL doesn\'t exist on INTERNET'
            })

    def __str__(self):
        return f'URL: {self.shortened_url}'
