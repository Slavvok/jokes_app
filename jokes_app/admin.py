from django.contrib import admin
from .models import Joke


class JokeAdmin(admin.ModelAdmin):
    fields = ('joke', )


admin.site.register(Joke, JokeAdmin)
