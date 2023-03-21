from django.test import TestCase, Client
from django.urls import reverse

class homePageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_renders(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')