from django.test import TestCase
from rest_framework.reverse import reverse

from .models import Resource
from rest_framework.test import APIClient
from rest_framework import status


# Create your tests here.

class ModelTestCase(TestCase):

    def setUp(self):
        self.resource_name = "test_resource"
        self.resource = Resource(name=self.resource_name)

    def test_model_can_create_a_resource(self):
        old_count = Resource.objects.count()
        self.resource.save()
        new_count = Resource.objects.count()
        self.assertEqual(old_count + 1, new_count)


class ViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.resource_data = {'name': 'Go to Ibiza'}
        self.response = self.client.post(
            reverse('create'),
            self.resource_data,
            format="json")

    def test_api_can_create_a_resource(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
