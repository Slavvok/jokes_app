from django.test import TestCase
from django.contrib.auth.models import User
from .views import *


class JokeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='testtest')
        self.client.login(username='test_user', password='testtest')

    def create_joke(self):
        Joke(joke="test joke").save(self.user)

    def test_generate_joke(self):
        response = self.client.get('/generate-joke')
        self.assertEqual(response.status_code, 200)

    def test_get_joke(self):
        self.create_joke()
        response = self.client.get('/get-joke/1', {"id": 1})
        self.assertEqual(response.status_code, 200)

    def test_get_jokes_list(self):
        response = self.client.get('/get-jokes-list')
        self.assertEqual(response.status_code, 200)

    def test_update_joke(self):
        self.create_joke()
        response = self.client.post('/update-joke/1', {"id": 1, "joke": "new joke"})
        self.assertEqual(response.status_code, 200)

    def test_remove_joke(self):
        self.create_joke()
        response = self.client.post('/remove-joke/1', {"id": 1})
        self.assertEqual(response.status_code, 200)
