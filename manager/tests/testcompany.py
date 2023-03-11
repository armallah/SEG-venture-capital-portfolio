from django.test import TestCase
from manager.models import Company

class CompanyTestCase(TestCase):
    def setUp(self):
        Company.objects.create(name = "company1", country_code = "UK")

    def testEmpty(self):
        company = Company.objects.first()
        if(company is None):
            self.fail("company was not created successfully")

    def testName(self):
        company = Company.objects.first()
        if(company is not None):
            self.assertEqual(company.name, "company1")

    def testCountryCode(self):
        company = Company.objects.first()
        if(company is not None):
            self.assertEqual(company.country_code, "UK")


    def testEmptyEntityRelation(self):
        firstCompany = Company.objects.first()
        if(firstCompany is not None):
            self.assertEqual(firstCompany.founders.count(), 0)
            self.assertEqual(firstCompany.investors.count(), 0)

    def testIsportfolio(self):
        ecosystem = Company.objects.first()
        portfolio = Company.objects.create(name = "company2", country_code="UK", wayra_investment = 5)
        self.assertFalse(ecosystem.isPortfolio())
        self.assertTrue(portfolio.isPortfolio())
