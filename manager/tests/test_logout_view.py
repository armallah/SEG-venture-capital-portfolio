from django.test import TestCase
from django.urls import reverse
from manager.models import User
# i got this from keats

class LogOutViewTestCase(TestCase): 
    

    def setUp(self): # creates demo objects just for testing
        self.url = reverse('log_out')
        self.user = User.objects.create_user(
            username = 'johndoe@example.org',
            first_name = 'John',
            last_name = 'Doe',
            password = 'Password123',
            user_type = 1
        )

    def test_log_out_url(self): # checks if the current url matches the log_out url
        self.assertEqual(self.url, '/log_out/')

    def test_get_log_out(self):
        self.client.login(username = 'johndoe@example.org', password = 'Password123') # logs user in
        response = self.client.get(self.url, follow = True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code =200) # redirects user to home page
        self.assertTemplateUsed(response, 'home.html') # makes sure user is in home page
        pass


    