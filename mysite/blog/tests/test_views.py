from django.test.testcases import TestCase
from django.urls import reverse

from . import factories

class PostListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.User = factories.RandomUserFactory()
        cls.User.save()
        
        number_of_posts = 20
        for _ in range(number_of_posts):
            post = factories.RandomPostFactory(author=cls.User)
            post.save()


    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_blog_all_view(self):
        response = self.client.get(reverse('blog:all'))
        self.assertEquals(response.status_code, 200)
        print(response.items())

    def test_right_template_used_by_views(self):
        response = self.client.get(reverse('blog:all'))
        self.assertEquals(response.status_code, 200)        
