from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from .views import *


class JokeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='testtest')
        self.client.login(username='test_user', password='testtest')
        Joke(joke="test joke").save()

    def test_generate_joke(self):
        response = self.client.get('/generate-joke')
        self.assertEqual(response.status_code, 200)

    def test_get_joke(self):
        response = self.client.post('/get-joke', {"id": 1})
        self.assertEqual(response.status_code, 200)

    def test_get_jokes_list(self):
        response = self.client.post('/get-jokes-list')
        self.assertEqual(response.status_code, 200)

    def test_update_joke(self):
        response = self.client.post('/update-joke', {"id": 1, "joke": "new joke"})
        self.assertEqual(response.status_code, 200)

    def test_remove_joke(self):
        response = self.client.post('/remove-joke', {"id": 1, "type": "joke"})
        self.assertEqual(response.status_code, 200)
