from django.test import TestCase
from manager.models import User
from django.core.exceptions import ValidationError
# Create your tests here.

# i got some from keats and the rest i did my self


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'jaydoe@example.org',first_name='Jane',last_name='Doe',password='Password123', user_type = 1)
        
    def test_vaild_user(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail("Test user is not vaild")
   
    def test_blank_username(self):
        self.user.username = ''
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_blank_password(self):
        self.user.password = ''
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_blank_first_name(self):
        self.user.first_name = ''
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_blank_last_name(self):
        self.user.last_name = ''
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _assert_thing_is_valid(self, message="A valid thing was rejected"):
        try:
            self.user.full_clean()
        except ValidationError:
            self.fail(message)

    def _assert_thing_is_invalid(self, message="An invalid thing was accepted"):
        try:
            self.user.full_clean()
            self.fail(message)
        except ValidationError:
            pass

    def test_first_name_may_have_30_characters(self):
        self.user.first_name = 'a' * 30
        self._assert_thing_is_valid(message="first name may have 30 characters")

    def test_first_name_must_not_have_more_than_30_characters(self):
        self.user.first_name = 'a' * 31
        self._assert_thing_is_invalid(message="first name must not have more than 30 characters")

    def test_last_name_may_have_30_characters(self):
        self.user.last_name = 'a' * 30
        self._assert_thing_is_valid(message="last name may have 30 characters")

    def test_last_name_must_not_have_more_than_30_characters(self):
        self.user.last_name = 'a' * 31
        self._assert_thing_is_invalid(message="last name must not have more than 30 characters")

    def test_email_may_have_50_characters(self):
        self.user.username = 'a' * 40 + '@gmail.com'
        self._assert_thing_is_valid(message="username may have 50 characters")

    def test_email_must_not_have_more_than_50_characters(self):
        self.user.username = 'dsjfbdhsfbshfdshbhbhgyuvygvyfdjfndskjfbsddfbdskfdbsfdbsksbfdskfbshkfhbkjqoqwiwqndwqjdndkqj@gmail.com'
        self._assert_thing_is_invalid(message="username must not have more than 50 characters")

    def test_user_type_is_positive(self):
        self.user.user_type = -1
        self._assert_thing_is_invalid(message="user type must be positive")

    def test_user_type_is_not_more_than_2(self):
        self.user.username = 3
        self._assert_thing_is_invalid(message="user type must be between 1 and 5 included")

    def test_valid_user_type(self):
        self.user.user_type = 1
        self._assert_thing_is_valid(message="user type is valid")
        self.user.user_type = 2
        self._assert_thing_is_valid(message="user type is valid")


    def test_invalid_user_type(self):
        self.user.username = 0
        self._assert_thing_is_invalid(message="user type must be 1 or 2")
        self.user.username = 1.9
        self._assert_thing_is_invalid(message="user type must be 1 or 2")



