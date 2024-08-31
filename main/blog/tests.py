from django.test import TestCase, SimpleTestCase
from blog.models import Author, BlogPost, Category
from django.utils import timezone
import datetime

class BlogPostTests(TestCase):
    def setUp(self):
        _author = Author.objects.create(
            name='bob stark',
            email='bob@stark.com'
        )

        _category = Category.objects.create(name='test_category')

        _blog_post = BlogPost.objects.create(
            title="Worldhood of the World",
            date=datetime.datetime.now(tz=timezone.utc),
            body="The deets",
            author=_author,
            slug="sluggy",
        )
        _blog_post.categories.set([_category])

    def test_author(self):
        author = Author.objects.get(email='bob@stark.com')
        self.assertEqual(author.name, 'bob stark')

    def test_blog_post_create(self):
        hello_blog = BlogPost.objects.get(title="Worldhood of the World")
        self.assertEqual(hello_blog.body, 'The deets')


class BlogHomePageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class ProjectsCFCTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/projects/chosenfewchildren/")
        self.assertEqual(response.status_code, 200)


class AboutpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)


class SoftwarepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/software/")
        self.assertEqual(response.status_code, 200)


class ProjectspageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/projects/")
        self.assertEqual(response.status_code, 200)


class SearchpageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/search/?q=test")
        self.assertEqual(response.status_code, 200)
