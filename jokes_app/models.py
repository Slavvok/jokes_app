from django.db import models


class Joke(models.Model):
    joke = models.TextField(unique=True)

    class Meta:
        ordering = ["joke"]

    def __str__(self):
        return f'{self.id} {self.joke}'
