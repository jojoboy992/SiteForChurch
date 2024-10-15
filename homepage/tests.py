# tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post
from django.core.exceptions import ValidationError
from django.urls import reverse
from .forms import PostForm

class PostModelTest(TestCase):

    def setUp(self):
        # Set up a user for the author field
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_post_creation(self):
        # Create a post with valid data
        post = Post.objects.create(
            title='Valid Title',
            content='This is a valid content with fewer than 150 characters.',
            author=self.user,
            published=True
        )
        # Check if the post was created successfully
        self.assertEqual(post.title, 'Valid Title')
        self.assertEqual(post.content, 'This is a valid content with fewer than 150 characters.')
        self.assertEqual(post.author, self.user)
        self.assertTrue(post.published)

    def test_post_title_max_length(self):
        # Try to create a post with a title longer than 30 characters
        long_title = 'A' * 31
        post = Post(
            title=long_title,
            content='This is valid content',
            author=self.user
        )
        # Validate the model to check the max length constraint
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_post_content_max_length(self):
        # Try to create a post with content longer than 150 characters
        long_content = 'A' * 151
        post = Post(
            title='Valid Title',
            content=long_content,
            author=self.user
        )
        # Validate the model to check the max length constraint
        with self.assertRaises(ValidationError):
            post.full_clean()


class PostViewTests(TestCase):

    def setUp(self):
        # Set up a test user and a superuser
        self.user = User.objects.create_user(username='user', password='password')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')

        # Create a sample post
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post content",
            author=self.admin_user,
            published=True  # Ensure this is True
        )

        # Create a test client
        self.client = Client()

    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_about_page_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_contact_page_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_post_list_view(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events-activities.html')
        self.assertContains(response, self.post.title)

    # def test_post_detail_view(self):
    #     response = self.client.get(reverse('post_detail', args=[self.post.pk]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'post_detail.html')
    #     self.assertContains(response, self.post.content)

    def test_post_new_view_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_post.html')

    def test_post_new_view_as_non_admin(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 404)  # Expecting a 404 for non-admin users

    def test_post_edit_view_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('post_edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_post.html')

    def test_post_edit_view_as_non_admin(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('post_edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 404)  # Expecting a 404 for non-admin users

    def test_post_delete_view_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertRedirects(response, reverse('blog'))

    def test_post_delete_view_as_non_admin(self):
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 404)  # Expecting a 404 for non-admin users
