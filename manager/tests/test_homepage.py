from django.test import TestCase, Client

class homePageTest(TestCase):
    def setUp(self):
        self.client = Client()