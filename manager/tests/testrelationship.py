from django.test import TestCase
from manager.models import Company, Entity, Investing
from django.core.exceptions import ValidationError

class InvestingTestCase(TestCase):
    def setUp(self):
        company = Company.objects.create(name = "company1", country_code="UK")
        entity = Entity.objects.create(name= "entity1")

        self.investing = Investing.objects.create(investor = entity, company = company, amount = 10.00)
        company.investors.add(entity)

    def testMirror(self):
        entity :Entity = Entity.objects.first() or self.fail("entity do not exits")
        company : Company = Company.objects.first() or self.fail("company do not exists")

        self.assertEqual(entity.invested_company.first(), company)
        self.assertEqual(company.investors.first(), entity)

    def testInvesting(self): 
        entity :Entity = Entity.objects.first() or self.fail("entity do not exits")
        company : Company = Company.objects.first() or self.fail("company do not exists")
        
        investing: Investing = Investing.objects.filter(investor = entity, company = company).first() or self.fail("investing do not exists")
        self.assertEqual(investing.amount, 10.00)
        self.assertEqual(investing.company, company)
        self.assertEqual(investing.investor, entity)

    def test_amount_may_have_20_characters(self):
        self.investing.amount = 11111111111111111
        self._assert_thing_is_valid(message="amount may have 17 digits before decimal points")

    def test_amount_must_not_have_more_than_20_characters(self):
        self.investing.amount = 111111111111111111
        self._assert_thing_is_invalid(message="amount name must not have more than 17 digits before decimal points")


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

class FoundingTestCase(TestCase):
    def setUp(self):
        company = Company.objects.create(name = "company1", country_code="UK")
        entity = Entity.objects.create(name="entity1")

        company.founders.add(entity)

    def testMirror(self):
        entity :Entity = Entity.objects.first() or self.fail("entity do not exits")
        company : Company = Company.objects.first() or self.fail("company do not exists")

        self.assertEqual(company.founders.first(), entity)
        self.assertEqual(entity.founding_company.first(), company)


