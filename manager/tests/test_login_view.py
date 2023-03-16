from django.test import TestCase
from manager.forms import LoginForm
from django.urls import reverse
from manager.models import Company, User
from django.contrib import messages, auth

# i got some from keats but i made the rest myself

class LogInViewTestCase(TestCase):
    """Tests of the login in view"""

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.create_user(
            user_type = 1,
            username = 'johndoe@example.org', 
            password =  'Password1234',
        )
        self.form_input = { 'username': 'johndoe@example.org', 'password': 'Password1234'}
        self.redirect_url = reverse('dashboard')

    def test_login_url(self): # checks if the url is the same as login url.
        self.assertEqual(self.url, '/login/')

    
    '''def checkForm(self,response): # checks the form
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginForm)) # checks that the form is a LoginForm
        self.assertFalse(form.is_bound) # checks the form is in bound'''

    def test_get_login(self): # checks that form is correct and that there are no error messages.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html') # checks if user is in the login page.
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginForm)) # checks that the form is a LoginForm
        self.assertFalse(form.is_bound) # checks the form is in bound
        messageList = list(response.context['messages'])
        self.assertEquals(len(messageList),0) # checks that there are no error messages.

    def test_unsuccesful_login(self): # checks if unsuccesful login is detected
        form_input = { 'username': 'johndoe@example.org', 'password': 'wrongpassword1234'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html') # checks if user is in the login page.
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginForm)) # checks that the form is a LoginForm
        self.assertFalse(form.is_bound) # checks the form is in bound
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated) # The user should not be logged in
        # self.assertFalse(self.logged_in()) # checks if user is logged in, should be false
        messageList = list(response.context['messages'])
        self.assertEquals(len(messageList),1) # checks that there is a message
        self.assertEquals(messageList[0].level, messages.ERROR) # checks that the message is an error message

    def test_succesful_login(self): # checks if succesful login is detected
        form_input = { 'username': 'johndoe@example.org', 'password': 'Password1234'}
        response = self.client.post(self.url, form_input, follow=True)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated) # test if the user is logged in
        self.assertEqual(user, self.user) # test if the logged in user is the same as the one created
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code =200) # redirects user to feed page
        self.assertTemplateUsed(response, 'dashboard.html')
        messageList = list(response.context['messages'])
        self.assertEquals(len(messageList),0) # checks that there are no messages