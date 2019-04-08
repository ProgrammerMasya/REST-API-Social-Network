from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from home.models import Post

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


User = get_user_model()


class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username="testcfeuser", email="test@test.com")
        user_obj.set_password("somerandopassword")
        user_obj.save()

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = Post.objects.count()
        self.assertEqual(post_count, 1)
