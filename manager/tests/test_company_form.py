from django.test import TestCase
from manager.models import User
from manager.forms import CompanyForm

# i created this my self

class CompanyFormTest(TestCase):
    """unit test of the company form"""

    def setUp(self):
        self.form_input = {
            'name': 'Jane Doe',
            'number': '12345',
            'country_code': 'Uk123',
            'wayra_investment': 10000.00,
            'description': 'Hello my name is Jane Doe',
            'founder_Name':'Janeathan Doe'
        }


    def test_valid_sign_up_form(self): # checks that the valid details are accepted
        form = CompanyForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_name(self): # checks that blank name is not allowed
        self.form_input['name'] = ''
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_number(self): # checks that blank number is not allowed
        self.form_input['number'] = ''
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_country_code(self): # checks that blank country code is not allowed
        self.form_input['country_code'] = ''
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_wayra_investment(self): # checks that blank wayra investment is not allowed
        self.form_input['wayra_investment'] = ''
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_wayra_investment_input(self): # checks that invalid inputs aren't accepted
        self.form_input['wayra_investment'] = -2
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['wayra_investment'] = -1.2
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['wayra_investment'] = -129.292
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['wayra_investment'] = -2918.0189
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['wayra_investment'] = 12345678910
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_name_may_have_50_characters(self):
        self.form_input['name'] = 'a' * 50
        form = CompanyForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_name_must_not_have_more_than_50_characters(self):
        self.form_input['name'] = 'a' * 51
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_number_may_have_50_characters(self):
        self.form_input['number'] = '1' * 50
        form = CompanyForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_number_must_not_have_more_than_50_characters(self):
        self.form_input['number'] = '1' * 51
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_country_code_may_have_15_characters(self):
        self.form_input['country_code'] = 'a' * 15
        form = CompanyForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_country_code_must_not_have_more_than_15_characters(self):
        self.form_input['country_code'] = 'a' * 16
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_description_may_have_200_characters(self):
        self.form_input['description'] = 'a' * 200
        form = CompanyForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_description_must_not_have_more_than_200_characters(self):
        self.form_input['description'] = 'a' * 201
        form = CompanyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    
