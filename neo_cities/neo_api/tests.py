import tempfile
from PIL import Image
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action


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
        # Check that the object was saved
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

    def test_api_created_resource_values_are_set(self):
        print(self.response.data)
        response_name = self.response.data['name']
        expected_name = self.resource_data['name']
        self.assertEqual(expected_name, response_name)

        # url = self.response.data['icon']
        # expected_icon = self.resource_data['icon']

        # response_icon = BytesIO(requests.get(url).content)

        # self.assertEqual(expected_icon, response_icon)
    # def test_api_model_resources(self):
    # image = self.create_test_image()
    # resource_data = {'name': 'Go to Ibiza', 'icon': image}
    # actual_data = self.post_set_up(resource_data, '/api/resources/').data
    # self.assert_dictionaries_equal(resource_data, actual_data, ['icon'])
    # self.assertEqual(self.get_image_from_url(actual_data['icon']), image)


class DynamicModelTestCase(TestCase):

    def create_test_image(self):
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')
        return open(f.name, mode='rb')

    def assert_dictionaries_equal(self, expected, actual, fields=None):
        if fields is None:
            fields = expected.keys()
        for key in fields:
            expected_value = expected[key]
            actual_value = actual[key]
            self.assertEqual(expected_value, actual_value, "expected: " + expected_value + "\n" + "actual: " + actual_value)


class TestData(DynamicModelTestCase):
    def get_model_manager(self):
        raise NotImplementedError()

    def get_model_instance(self):
        raise NotImplementedError()

    def get_api_data(self):
        raise NotImplementedError()

    def get_api_url_path(self):
        raise NotImplementedError()

    def assert_model_can_create(self):
        manager = self.get_model_manager()
        model_instance = self.get_model_instance()
        old_count = manager.objects.count()
        model_instance.save()
        new_count = manager.objects.count()
        self.assertEqual(old_count + 1, new_count)

    def assert_api_post(self):
        model_data = self.get_api_data()
        client = APIClient()
        response = client.post(self.get_api_url_path(), model_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ResourceTestDataCase(TestData):
    def get_model_manager(self):
        return Resource

    def get_model_instance(self):
        resource_name = "test_resource"
        return Resource(name=resource_name)

    def get_api_data(self):
        image = self.create_test_image()
        return {'name': 'Go to Ibiza', 'icon': image}

    def get_api_url_path(self):
        return '/api/resources/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


class EventTestDataCase(TestData):
    def get_model_manager(self):
        return Event

    def get_model_instance(self):
        from django.db.models.functions import Now
        return Event(
            success_resources=Threshold(),
            icon=self.create_test_image(),
            start_time=Now(),
            description='test desc',
            details='test details')

    def get_api_data(self):
        image = self.create_test_image()
        return {'name': 'Go to Ibiza', 'icon': image}

    def get_api_url_path(self):
        return '/api/events/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()
