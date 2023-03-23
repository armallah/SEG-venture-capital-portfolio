from django.test import TestCase
from manager.models import Company, Right
from django.core.exceptions import ValidationError

class RightTestCase(TestCase):
    def setUp(self):
        company1 = Company.objects.create(name="company1", country_code = "UK")
        right1 = Right.objects.create(name = "right1")
        company2 = Company.objects.create(name="company2", country_code = "UK")
        right2 = Right.objects.create(name = "right2")
        self.right1 = right1
        self.right2 = right2

        right1.holding_right.add(company1)
        right1.holding_right.add(company2)
        right2.holding_right.add(company1)
        pass

    def testRightMirror(self):
        company1 = Company.objects.filter(name = "company1").first() or self.fail("company1 do not exist")
        right1 = Right.objects.filter(name = "right1").first() or self.fail("right1 do not exist")

        self.assertEqual(company1.wayra_right.first(), right1)
        self.assertEqual(right1.holding_right.first(), company1)

    def testRightMultiple(self):
        company1 = Company.objects.filter(name = "company1").first() or self.fail("company1 do not exist")
        company2 = Company.objects.filter(name = "company2").first() or self.fail("company2 do not exist")
        right1 = Right.objects.filter(name = "right1").first() or self.fail("right1 do not exist")
        right2 = Right.objects.filter(name = "right2").first() or self.fail("right2 do not exist")

        self.assertTrue(right1 in company2.wayra_right.all())
        self.assertTrue(right2 in company1.wayra_right.all())
        self.assertTrue(right1 in company2.wayra_right.all())
        self.assertFalse(right2 in company2.wayra_right.all())

        self.assertTrue(company1 in right1.holding_right.all())
        self.assertTrue(company1 in right2.holding_right.all())
        self.assertTrue(company2 in right1.holding_right.all())
        self.assertFalse(company2 in right2.holding_right.all())

    def test_name_may_have_50_characters(self):
        self.right1.name = 'a' * 50
        self._assert_thing_is_valid(message="name may have 50 characters")

    def test_number_must_not_have_more_than_50_characters(self):
        self.right1.name = 'a' * 51
        self._assert_thing_is_invalid(message=" name must not have more than 50 characters")


    def _assert_thing_is_valid(self, message="A valid thing was rejected"):
        try:
            self.right1.full_clean()
        except ValidationError:
            self.fail(message)

    def _assert_thing_is_invalid(self, message="An invalid thing was accepted"):
        try:
            self.right1.full_clean()
            self.fail(message)
        except ValidationError:
            pass