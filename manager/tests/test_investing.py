from django.test import TestCase
from manager.models import Investing, Company, Entity
from django.core.exceptions import ValidationError


class InvestingTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name = "company1", country_code = "UK", number = "ABC015")
        self.investor = Entity.objects.create(name = "test")
        self.investing = Investing.objects.create(investor = self.investor, company = self.company, amount = 10000)
    
    def test_vaild_investing(self):
        try:
            self.company.full_clean()
            self.investor.full_clean()
            self.investing.full_clean()

        except (ValidationError):
            self.fail("Test investing is not vaild")
    

    def testEmpty(self):
        investing = Investing.objects.first()
        if(self.investing is None):
            self.fail("investing was not created successfully")

    def testEmptyCompany(self):
        try:
            self.investing.company = ''
        except:
            self._assert_thing_is_valid(message="Company can not be empty")
            self.investing.full_clean()
    
    def testEmptyInvestor(self):
        try:
            self.investing.investor = ''
        except:
            self._assert_thing_is_valid(message="Investor cannot be empty")
            self.investing.full_clean()


    def test_amount_may_have_20_characters(self):
        self.investing.amount = 11111111111111111.111
        self._assert_thing_is_valid(message="amount may have 17 digits before decimal points")

    def test_amount_must_not_have_more_than_20_characters(self):
        self.investing.amount = 111111111111111111.111
        self._assert_thing_is_invalid(message="amount may not have more than 17 digits before decimal points")

    def test_invalid_amount_inputs(self):
        self.investing.amount = -111
        self._assert_thing_is_invalid(message="amount must be positive")
        self.investing.amount = -1.23
        self._assert_thing_is_invalid(message="amount must be positive")
        self.investing.amount = -2943839.39393930
        self._assert_thing_is_invalid(message="amount must be positive")
        self.investing.amount = ''
        self._assert_thing_is_invalid(message="amount must be positive")
        self.investing.amount = "skdnfsjn"
        self._assert_thing_is_invalid(message="amount must be positive")
        


    def _assert_thing_is_valid(self, message="A valid thing was rejected"):
        try:
            self.investing.full_clean()
        except ValidationError:
            self.fail(message)

    def _assert_thing_is_invalid(self, message="An invalid thing was accepted"):
        try:
            self.investing.full_clean()
            self.fail(message)
        except ValidationError:
            pass
 


