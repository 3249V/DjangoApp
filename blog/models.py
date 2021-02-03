from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

class Post(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField(max_length=100, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.FileField(upload_to='mememedia/',default="")

    def __str__(self):
        return self.title

    def clean(self):
        megabyte_limit = 5.0
        print(self.media.size)
        if self.media.size > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Suggestion(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog-home')