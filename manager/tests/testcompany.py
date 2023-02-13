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
