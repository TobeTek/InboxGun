from django.test.testcases import TestCase
from . import factories
import factory


class PostTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.User = factories.RandomUserFactory()
        cls.User.save()

    def setUp(self):
        self.post = factories.RandomPostFactory(author=PostTestCase.User)
        self.post.save()

    def test_get_absolute_url(self):
        self.assertEquals(self.post.get_absolute_url(), f"/blog/read/{self.post.slug}")

    def test_str_representation(self):
        self.assertEqual(str(self.post), f"{self.post.title}")

    def test_max_length_for_title(self):
        max_length = self.post._meta.get_field("title").max_length
        self.assertEquals(max_length, 250)

    def test_max_length_for_slug(self):
        max_length = self.post._meta.get_field("slug").max_length
        self.assertEquals(max_length, 300)
