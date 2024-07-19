from django.db import models
import string
import random

def generate_short_url():
    length = 6
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choices(characters, k=length))
        if not ShortURL.objects.filter(short_url=short_url).exists():
            return short_url

class ShortURL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=6, unique=True, default=generate_short_url)
    created_at = models.DateTimeField(auto_now_add=True)
