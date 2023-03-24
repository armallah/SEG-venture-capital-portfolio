from django.test import TestCase
from manager.models import Company
from manager.forms import RoundForm
import datetime


# i created this my self

class RoundFormTest(TestCase):
    """unit test of the round form"""

    def setUp(self):
        self.company = self.company = Company.objects.create(name = "company1", country_code = "UK", number = "ABC015")

        self.form_input = {
            'company': self.company,
            'round_number': 1,
            'equity': 10000.00,
            'wayra_equity': 2000.00,
            'pre_money_valuation': 3000.00,
        }
    
    def test_valid_sign_up_form(self): # checks that the valid details are accepted
        form = RoundForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_blank_company(self): # checks that blank company is not allowed
        self.form_input['company'] = ''
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_round_number(self): # checks that blank round number is not allowed
        self.form_input['round_number'] = ''
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_equity(self): # checks that blank equity is not allowed
        self.form_input['equity'] = ''
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_wayra_equity(self): # checks that blank wayra_equity is not allowed
        self.form_input['wayra_equity'] = ''
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_pre_money_valuation(self): # checks that blank pre_money_valuation is not allowed
        self.form_input['pre_money_valuation'] = ''
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_round_numbers(self): # checks if invalid round numbers are rejeected
        self.form_input['round_number'] = -1
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['round_number'] = -1.39
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['round_number'] = 2.48
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    def test_invalid_equity(self): # checks if invalid equitys are rejeected
        self.form_input['equity'] = -1
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['equity'] = -1383.39
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['equity'] = 54747379562754725462457524932459
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['equity'] = "ejhdbf"
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    
    def test_invalid_wayra_equity(self): # checks if invalid wayra_equitys are rejeected
        self.form_input['wayra_equity'] = -23
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['wayra_equity'] = -193.2
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['wayra_equity'] = 27392723982837338293728292928
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['wayra_equity'] = "sjsndndjbf"
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_pre_money_valuation(self): # checks if invalid pre_money_valuations are rejeected
        self.form_input['pre_money_valuation'] = -29
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['pre_money_valuation'] = -3728.27227
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['pre_money_valuation'] = 373849272928293372328373392827
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.form_input['pre_money_valuation'] = "adsasfnsak"
        form = RoundForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    
        