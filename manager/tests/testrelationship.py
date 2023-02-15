from django.test import TestCase
from manager.models import Company, Entity, Investing

class InvestingTestCase(TestCase):
    def setUp(self):
        company = Company.objects.create(name = "company1", country_code="UK")
        entity = Entity.objects.create(name= "entity1")

        Investing.objects.create(investor = entity, company = company, amount = 10.00)
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


