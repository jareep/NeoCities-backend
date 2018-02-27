from django.test import TestCase
from rest_framework.reverse import reverse

from .models import Resource
from rest_framework.test import APIClient
from rest_framework import status
from PIL import Image
import tempfile
# Create your tests here.

class ResourceModelTestCase(TestCase):

    def setUp(self):
        # Create the object with all of it's values
        self.resource_name = "test_resource"
        self.resource = Resource(name=self.resource_name)

    def test_model_can_create_a_resource(self):
        old_count = Resource.objects.count()
        # Save the object
        self.resource.save()
        new_count = Resource.objects.count()
        # Check that the object was savedk
        self.assertEqual(old_count + 1, new_count)



class ResourceViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        with open(tmp_file.name, 'rb') as data:
            self.resource_data = {'name': 'Go to Ibiza', 'icon': data}
            # TODO use reverse instead of hard coded URL /api/resources/
            self.response = self.client.post(
                '/api/resources/',
                self.resource_data)
            # TODO Check resource_data to make sure everything was saved and the format is correct

    def test_api_can_create_a_resource(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
