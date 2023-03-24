from django.test import TestCase
from manager.models import User
from manager.forms import FounderForm

# i created this my self

class FounderFormTest(TestCase):
    """unit test of the founder form"""

    def setUp(self):
        self.form_input = {
            'name': 'Jane Doe',
            'company': 'wayra_investment',
        }
    
    def test_valid_sign_up_form(self): # checks that the valid details are accepted
        form = FounderForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_name(self): # checks that blank name is not allowed
        self.form_input['name'] = ''
        form = FounderForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_number(self): # checks that blank company is not allowed
        self.form_input['company'] = ''
        form = FounderForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_name_may_have_50_characters(self):
        self.form_input['name'] = 'a' * 50
        form = FounderForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_name_must_not_have_more_than_50_characters(self):
        self.form_input['name'] = 'a' * 51
        form = FounderForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_company_may_have_50_characters(self):
        self.form_input['company'] = 'a' * 50
        form = FounderForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_company_must_not_have_more_than_50_characters(self):
        self.form_input['company'] = 'a' * 51
        form = FounderForm(data=self.form_input)
        self.assertFalse(form.is_valid())


        
