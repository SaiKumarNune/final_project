from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

class BasicViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_homepage_requires_login(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/login/?next=/')


    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home

    def test_disease_page_loads(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('disease'))
        self.assertEqual(response.status_code, 200)

    def test_disease_prediction_no_file(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('disease_prediction'), {})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.url)

