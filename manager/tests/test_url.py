from django.test import TestCase
from django.urls import reverse

class UrlTestCase(TestCase):
    """Tests of the Urls"""

    def setUp(self):

        self.url = ""

    def test_url(self):

        self.url = reverse('home')
        self.assertEqual(self.url, '/')

        self.url = reverse('sync airtable')
        self.assertEqual(self.url, '/sync/')

        self.url = reverse('log_in')
        self.assertEqual(self.url, '/login/')

        self.url = reverse('log_out')
        self.assertEqual(self.url, '/log_out/')

        self.url = reverse('dashboard')
        self.assertEqual(self.url, '/dashboard/')

        self.url = reverse('adminDashboard')
        self.assertEqual(self.url, '/adminDashboard/')

        self.url = reverse('portfolio')
        self.assertEqual(self.url, '/portfolio/')
        
        self.url = reverse('adminPortfolio')
        self.assertEqual(self.url, '/adminPortfolio/')

        self.url = reverse('entities')
        self.assertEqual(self.url, '/entities/')

        self.url = reverse('adminEntities')
        self.assertEqual(self.url, '/adminEntities/')

        self.url = reverse('founders')
        self.assertEqual(self.url, '/founders/')

        self.url = reverse('adminFounders')
        self.assertEqual(self.url, '/adminFounders/')

        self.url = reverse('ecosystem')
        self.assertEqual(self.url, '/ecosystem/')

        self.url = reverse('adminEcosystem')
        self.assertEqual(self.url, '/adminEcosystem/')

        self.url = reverse('users')
        self.assertEqual(self.url, '/users/')

        self.url = reverse('adminAddUser')
        self.assertEqual(self.url, '/adminAddUser/')

        self.url = reverse('adminProhibitted')
        self.assertEqual(self.url, '/adminProhibitted/')

        self.url = reverse('reset_password')
        self.assertEqual(self.url, '/reset_password')

        self.url = reverse('password_reset_done')
        self.assertEqual(self.url, '/reset_password_sent')

        self.url = reverse('password_reset_complete')
        self.assertEqual(self.url, '/reset_password_complete/')



