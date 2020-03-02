from django.urls import path
from .views2 import *


urlpatterns = [
    # path('generate-joke', generate_joke, name='generate_joke'),
    path('generate-joke', GenerateJokeView.as_view(), name='generate_joke'),
    path('get-joke/<int:pk>', GetJokeView.as_view(), name='get_joke'),
    path('get-jokes-list', GetJokesListView.as_view(), name='get_jokes_list'),
    path('update-joke/<int:pk>', update_joke, name='update_joke'),
    path('remove-joke/<int:pk>', remove_joke, name='remove_joke'),
    path('auth/login', user_login, name='login'),
    path('auth/logout', user_logout, name='logout'),
    path('auth/registration', user_registration, name='registration')
]
