from django.test import TestCase
from manager.models import Round, Company
from django.core.exceptions import ValidationError
import datetime

class RoundTestCase(TestCase):
    def setUp(self):
        company1 = Company.objects.create(name="company1", country_code = "UK")
        self.round = Round.objects.create(Company = company1, round_number = 3, equity = 2000.00, wayra_equity = 2000.00, pre_money_valuation = 3000.00, round_date = datetime.date(2023, 3, 18))
        pass

    def test_vaild_round(self):
        try:
            self.round.full_clean()

        except (ValidationError):
            self.fail("Test company is not vaild")
    

    def testEmpty(self):
        
        if(self.round is None):
            self.fail("round was not created successfully")

    def test_round_number_may_have_5_characters(self):
        self.round.round_number = 11111
        self._assert_thing_is_valid(message="round_number may have 5 characters")

    def test_round_number_must_not_have_more_than_5_characters(self):
        self.round.round_number = 111111
        self._assert_thing_is_invalid(message=" round_number must not have more than 5 characters")

    def test_equity_may_have_20_characters(self):
        self.round.equity = 11111111111111111111
        self._assert_thing_is_valid(message="equity may have 20 characters")

    def test_equity_must_not_have_more_than_20_characters(self):
        self.round.equity = 111111111111111111111
        self._assert_thing_is_invalid(message=" equity must not have more than 20 characters")

    def test_wayra_equity_may_have_20_characters(self):
        self.round.wayra_equity = 11111111111111111111
        self._assert_thing_is_valid(message="wayra_equity may have 20 characters")

    def test_wayra_equity_must_not_have_more_than_20_characters(self):
        self.round.wayra_equity = 111111111111111111111
        self._assert_thing_is_invalid(message="wayra_equity must not have more than 20 characters")

    def test_pre_money_valuation_may_have_20_characters(self):
        self.round.pre_money_valuation = 11111111111111111111
        self._assert_thing_is_valid(message="pre_money_valuation may have 20 characters")

    def test_pre_money_valuation_must_not_have_more_than_20_characters(self):
        self.round.pre_money_valuation = 111111111111111111111
        self._assert_thing_is_invalid(message="pre_money_valuation must not have more than 20 characters")

    def test_round_number_min(self):
        self.round.round_number = -1
        self._assert_thing_is_invalid(message="round_number must be positive")
        
    def test_equity_min(self):
        self.round.equity = -1
        self._assert_thing_is_invalid(message="equity must be positive")

    def test_wayra_equity_min(self):
        self.round.wayra_equity = -1
        self._assert_thing_is_invalid(message="wayra_equity must be positive")
        
    def test_pre_money_valuation_min(self):
        self.round.pre_money_valuation = -1
        self._assert_thing_is_invalid(message="pre_money_valuation must be positive")
        
    def _assert_thing_is_valid(self, message="A valid thing was rejected"):
        try:
            self.round.full_clean()
        except ValidationError:
            self.fail(message)

    def _assert_thing_is_invalid(self, message="An invalid thing was accepted"):
        try:
            self.round.full_clean()
            self.fail(message)
        except ValidationError:
            pass