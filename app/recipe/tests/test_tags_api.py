"""Tests for the tags API."""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URLS = reverse('recipe:tag-list')


def create_user(email='user@example.com', password='test123'):
    """Create and return a new usaer."""
    return get_user_model().objects.create_user(email, password)


def create_tag(user, **params):
    return Tag.objects.create(user=user, **params)


def detail_url(tag_id):
    """Create and return tag detgail url."""
    return reverse('recipe:tag-detail', args=(tag_id,))


class PublicTagsApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth required for retrieveing tags."""

        res = self.client.get(TAGS_URLS)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieve a list of tags."""
        create_tag(user=self.user, name="Vegan")
        create_tag(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URLS)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(tags.count(), 2)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Retrieving tags assigned to logged in user."""
        other_user = create_user(email='other@exaple.com', password='other123')
        create_tag(user=self.user, name="Vegan")
        create_tag(user=self.user, name="Dessert")
        create_tag(user=other_user, name="Looser")

        res = self.client.get(TAGS_URLS)
        tags = Tag.objects.filter(id=self.user.id)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        for tag in tags:
            self.assertEqual(tag.user, self.user)

    def test_update_tags(self):
        """Update tag successfully assigned to logged in user."""
        tag = create_tag(user=self.user, name="Tag")
        url = detail_url(tag.id)
        payload = {
            "name": "Updated tag"
        }

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Delete tag"""
        tag = create_tag(user=self.user, name="Asgard")
        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tag = Tag.objects.filter(user=self.user)
        self.assertFalse(tag.exists())


