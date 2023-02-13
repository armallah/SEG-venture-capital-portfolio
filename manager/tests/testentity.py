from django.test import TestCase
from manager.models import Entity
# Create your tests here.

class EntityTestCase(TestCase):
    def setUp(self):
        Entity.objects.create(name = "test")

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


