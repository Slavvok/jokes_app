from django.db import models
from django.contrib.auth.models import User


class Joke(models.Model):
    joke = models.TextField(unique=True)
    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["joke"]

    def __str__(self):
        if self.id is not None:
            return f'{self.pk} {self.joke}'
        else:
            return f'{self.joke}'

    def save(self, user='', *args, **kwargs):
        self.added_by = user
        super(Joke, self).save(*args, **kwargs)
