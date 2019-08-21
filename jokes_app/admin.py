from django.contrib import admin
from .models import Joke


class JokeAdmin(admin.ModelAdmin):
    fields = ('joke', )
    exclude = ('added_by', )


admin.site.register(Joke, JokeAdmin)
