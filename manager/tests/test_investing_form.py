from django.test import TestCase
from manager.models import User, Entity, Company
from manager.forms import InvestorForm

# i created this my self

class InvestortFormTest(TestCase):
    """unit test of the signup form"""

    def setUp(self):
        self.name = Entity.objects.create(name = "Jane")
        self.company = Company.objects.create(name = "company1", country_code = "UK", number = "ABC015")
        self.form_input = {
            'name': self.name,
            'company': self.company,
            'amount': 100000
        }
    
    def test_valid_sign_up_form(self): # checks that the valid details are accepted
        form = InvestorForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_name(self): # checks that blank investor is not allowed
        self.form_input['name'] = ''
        form = InvestorForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_number(self): # checks that blank company is not allowed
        self.form_input['company'] = ''
        form = InvestorForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_amount_inputs(self):
        self.form_input['amount'] = ''
        form = InvestorForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['amount'] = -239
        form = InvestorForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['amount'] = -28.39383
        form = InvestorForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['amount'] = -28327498238.339
        form = InvestorForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['amount'] = 'Hello'
        form = InvestorForm(data=self.form_input)
        self.assertFalse(form.is_valid())
