from django.urls import path, include
from .views import *


urlpatterns = [
    path('generate-joke', generate_joke, name='generate_joke'),
    path('get-joke', get_joke, name='get_joke'),
    path('get-jokes-list', get_jokes_list, name='get_jokes_list'),
    path('update-joke', update_joke, name='update_joke'),
    path('remove-joke', remove_joke, name='remove_joke'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout')
]
