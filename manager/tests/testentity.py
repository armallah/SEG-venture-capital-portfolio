from django.test import TestCase
from manager.models import Entity
from django.core.exceptions import ValidationError

# Create your tests here.

class EntityTestCase(TestCase):
    def setUp(self):
        self.entity = Entity.objects.create(name = "test")

    def test_vaild_entity(self):
        try:
            self.entity.full_clean()

        except (ValidationError):
            self.fail("Test entity is not vaild")
    

    def testNone(self):
        firstEntity = Entity.objects.first()

        if(firstEntity is None):
            self.fail("entity is none")

    def testName(self):
        firstEntity = Entity.objects.first()

        if(firstEntity is not None):
            self.assertEqual(firstEntity.getName(), "test")

    def testEmptyCompanyRelation(self):
        firstEntity = Entity.objects.first()
        if(firstEntity is not None):
            self.assertEqual(firstEntity.invested_company.count(), 0)
            self.assertEqual(firstEntity.founding_company.count(), 0)

    def test_blank_name(self):
        self.entity.name = ''
        with self.assertRaises(ValidationError):
            self.entity.full_clean()

    def test_blank_number(self):
        self.entity.number = ''
        with self.assertRaises(ValidationError):
            self.entity.full_clean()

    def test_name_may_have_50_characters(self):
        self.entity.name = 'a' * 50
        self._assert_thing_is_valid(message="name may have 30 characters")

    def test_name_must_not_have_more_than_50_characters(self):
        self.entity.name = 'a' * 51
        self._assert_thing_is_invalid(message="name must not have more than 30 characters")


    def _assert_thing_is_valid(self, message="A valid thing was rejected"):
        try:
            self.entity.full_clean()
        except ValidationError:
            self.fail(message)

    def _assert_thing_is_invalid(self, message="An invalid thing was accepted"):
        try:
            self.entity.full_clean()
            self.fail(message)
        except ValidationError:
            pass
