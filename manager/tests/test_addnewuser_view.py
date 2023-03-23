from django.test import TestCase
from manager.forms import AddNewUser
from django.urls import reverse
from manager.models import User

# i got most from keats and the rest i did myself


class AddNewUserViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='username',
            password='password',
            user_type = 2 
        )
        
        self.client.login(username='username', password='password')


        self.url = reverse('adminAddUser')
        self.form_input = {
            'first_name': 'Jay',
            'last_name': 'Doe',
            'email': 'jaydoe@example.org',
            'password': 'Password1234',
            'password_confirmation': 'Password1234'
        }
        self.redirect_url = reverse('home')
    
    def test_successful_sign_up(self): # checks that unsuccessful sign up is detected
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True) # creates new user
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1) # checks that a new user is created
        

    def test_sign_up_url(self): # checks if the url is the same as sign up url.
        self.assertEqual(self.url, '/adminAddUser/')

    def checkForm(self,response): # checks the form
        form = response.context['form']
        self.assertTrue(isinstance(form, AddNewUser)) # checks that the form is a SignUpForm
        self.assertFalse(form.is_bound) # checks that the form is in bound'''

    def test_get_sign_up(self): 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, AddNewUser)) # checks that the form is a SignUpForm
        self.assertFalse(form.is_bound)

    def test_unsuccessful_sign_up(self):  # checks that unsuccessful sign up is detected
        self.form_input['email'] = 'BAD_NAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count) # checks that no new user is created
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, AddNewUser)) # checks that the form is a SignUpForm
        self.assertTrue(form.is_bound)
