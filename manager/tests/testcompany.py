from django.test import TestCase
from manager.models import Company
from django.core.exceptions import ValidationError


class CompanyTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name = "company1", country_code = "UK")

    def test_vaild_company(self):
        try:
            self.company.full_clean()

        except (ValidationError):
            self.fail("Test company is not vaild")
    

    def testEmpty(self):
        company = Company.objects.first()
        if(self.company is None):
            self.fail("company was not created successfully")

    def testName(self):
        company = Company.objects.first()
        if(self.company is not None):
            self.assertEqual(company.name, "company1")

    def testCountryCode(self):
        company = Company.objects.first()
        if(self.company is not None):
            self.assertEqual(company.country_code, "UK")


    def testEmptyEntityRelation(self):
        firstCompany = Company.objects.first()
        if(firstCompany is not None):
            self.assertEqual(firstCompany.founders.count(), 0)
            self.assertEqual(firstCompany.investors.count(), 0)

    def test_blank_name(self):
        self.company.name = ''
        with self.assertRaises(ValidationError):
            self.company.full_clean()

    def test_blank_number(self):
        self.company.number = ''
        with self.assertRaises(ValidationError):
            self.company.full_clean()

    def test_name_may_have_50_characters(self):
        self.company.name = 'a' * 50
        self._assert_thing_is_valid(message="name may have 30 characters")

    def test_name_must_not_have_more_than_50_characters(self):
        self.company.name = 'a' * 51
        self._assert_thing_is_invalid(message="name must not have more than 30 characters")

    def test_number_may_have_50_characters(self):
        self.company.number = '1' * 50
        self._assert_thing_is_valid(message="number may have 30 characters")

    def test_number_must_not_have_more_than_50_characters(self):
        self.company.number = '1' * 51
        self._assert_thing_is_invalid(message="number name must not have more than 30 characters")


    def _assert_thing_is_valid(self, message="A valid thing was rejected"):
        try:
            self.company.full_clean()
        except ValidationError:
            self.fail(message)

    def _assert_thing_is_invalid(self, message="An invalid thing was accepted"):
        try:
            self.company.full_clean()
            self.fail(message)
        except ValidationError:
            pass
    
