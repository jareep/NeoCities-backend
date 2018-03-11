import tempfile
from PIL import Image
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.db.models.functions import Now
from datetime import datetime
from django.core.files import File

from .models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, Session, Action


class DynamicModelTestCase(TestCase):
    @staticmethod
    def create_test_api_image():
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')
        return open(f.name, mode='rb')

    @staticmethod
    def create_test_image():
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')
        return f.name

    def assert_dictionaries_equal(self, expected, actual, fields=None):
        if fields is None:
            fields = expected.keys()
        for key in fields:
            expected_value = expected[key]
            actual_value = actual[key]
            self.assertEqual(expected_value, actual_value, "expected: " + expected_value + "\n" + "actual: " + actual_value)


class TestData(DynamicModelTestCase):
    @classmethod
    def get_model_manager(cls):
        raise NotImplementedError()

    @classmethod
    def get_model_instance(cls):
        raise NotImplementedError()

    @classmethod
    def get_api_data(cls):
        raise NotImplementedError()

    @classmethod
    def get_api_url_path(cls):
        raise NotImplementedError()

    @classmethod
    def api_post(cls):
        return APIClient().post(cls.get_api_url_path(), cls.get_api_data())

    @classmethod
    def model_create(cls):
        model_instance = cls.get_model_instance()
        model_instance.save()
        return model_instance

    @classmethod
    def post_and_grab_id(cls):
        print(cls.api_post().data)
        return cls.api_post().data["id"]

    def assert_model_can_create(self):
        manager = self.get_model_manager()
        old_count = manager.objects.count()
        self.model_create()
        new_count = manager.objects.count()
        self.assertEqual(old_count + 1, new_count,
                         " where class = " + self.__class__.__name__)

    def assert_api_post(self):
        response = self.api_post()
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         " where class = " + self.__class__.__name__)


class ResourceTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return Resource

    @classmethod
    def get_model_instance(cls):
        return Resource(name="test_resource")

    @classmethod
    def get_api_data(cls):
        image = cls.create_test_api_image()
        return {'name': 'Go to Ibiza', 'icon': image}

    @classmethod
    def get_api_url_path(cls):
        return '/api/resources/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


class EventTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return Event

    @classmethod
    def get_model_instance(cls):
        return Event(
            icon=cls.create_test_image(),
            start_time=Now(),
            description='test desc',
            details='test details')

    @classmethod
    def get_api_data(cls):
        image = cls.create_test_api_image()
        return {
            'name': 'Go to Ibiza',
            'icon': image,
            'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'description': "test desc",
            'details': "test details"
        }

    @classmethod
    def get_api_url_path(cls):
        return '/api/events/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


class ThresholdTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return Threshold

    @classmethod
    def get_model_instance(cls):
        return Threshold(
            order=1,
            amount=42,
            enforce_order=False,
            resource=ResourceTest.model_create(),
            event=EventTest.model_create())

    @classmethod
    def get_api_data(cls):
        return {
            'order': 1,
            'amount': 42,
            'enforce_order': False,
            'resource': ResourceTest.post_and_grab_id(),
            'event': EventTest.post_and_grab_id()
        }

    @classmethod
    def get_api_url_path(cls):
        return '/api/threshold/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


class RoleTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return Role

    @classmethod
    def get_model_instance(cls):
        return Role(
            name='test name',
            icon=cls.create_test_image()
        )

    @classmethod
    def get_api_data(cls):
        return {
            'name': 'test name',
            'icon': cls.create_test_api_image()
        }

    @classmethod
    def get_api_url_path(cls):
        return '/api/role/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


class ResourceDepotTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return ResourceDepot

    @classmethod
    def get_model_instance(cls):
        return ResourceDepot(
            quantity=1,
            role=RoleTest.model_create(),
            resource=ResourceTest.model_create()
        )

    @classmethod
    def get_api_data(cls):
        return {
            'quantity': 1,
            'role': RoleTest.post_and_grab_id(),
            'resource': ResourceTest.post_and_grab_id()
        }

    @classmethod
    def get_api_url_path(cls):
        return '/api/resourcesdepot/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


class ScenarioTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return Scenario

    @classmethod
    def get_model_instance(cls):
        return Scenario(
        )

    @classmethod
    def get_api_data(cls):
        return {
        }

    @classmethod
    def get_api_url_path(cls):
        return '/api/scenario/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


class BriefingTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return Briefing

    @classmethod
    def get_model_instance(cls):
        return Briefing(
            details="test details for briefing",
            role=RoleTest.model_create(),
            scenario=ScenarioTest.model_create()
        )

    @classmethod
    def get_api_data(cls):
        return {
            'details': 'test details',
            'role': RoleTest.post_and_grab_id(),
            'scenario': ScenarioTest.api_post()
        }

    @classmethod
    def get_api_url_path(cls):
        return '/api/briefing/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


# Logging info


class ScoreTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return Score

    @classmethod
    def get_model_instance(cls):
        return Score(
            quant_score=1.1
        )

    @classmethod
    def get_api_data(cls):
        return {
            'quant_score': 0
        }

    @classmethod
    def get_api_url_path(cls):
        return '/api/score/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


class SessionTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return Session

    @classmethod
    def get_model_instance(cls):
        return Session(
            scenario_ran=ScenarioTest.model_create(),
            created_at=Now(),
            proctorNotes='test proctor notes',
            sessionNotes='test session notes'
        )

    @classmethod
    def get_api_data(cls):
        return {
            'scenario_ran': ScenarioTest.post_and_grab_id(),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'proctorNotes': 'test proctor notes',
            'sessionNotes': 'test session notes'
        }

    @classmethod
    def get_api_url_path(cls):
        return '/api/session/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


class ParticipantTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return Participant

    @classmethod
    def get_model_instance(cls):
        return Participant(
            name='test name',
            token='test token',
            session=SessionTest.model_create(),
            role=RoleTest.model_create(),
            score=ScoreTest.model_create()
        )

    @classmethod
    def get_api_data(cls):
        return {
            'name': 'test name',
            'token': 'test token',
            'session': SessionTest.api_post(),
            'role': RoleTest.post_and_grab_id(),
            'score': ScoreTest.post_and_grab_id()
        }

    @classmethod
    def get_api_url_path(cls):
        return '/api/participant/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()


class ActionTest(TestData):
    @classmethod
    def get_model_manager(cls):
        return Action

    @classmethod
    def get_model_instance(cls):
        return Action(
            timestamp=Now(),
            action_type=False,
            session=SessionTest.model_create(),
            participant=ParticipantTest.model_create(),
            quantity=2,
            event=EventTest.model_create()
        )

    @classmethod
    def get_api_data(cls):
        print(SessionTest.api_post().data)
        return {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'action_type': False,
            'session': SessionTest.api_post().data['id'],
            'participant': ParticipantTest.api_post(),
            'quantity': 2,
            # 'resource': ResourceTest.api_post(),
            'event': EventTest.post_and_grab_id()
        }

    @classmethod
    def get_api_url_path(cls):
        return '/api/action/'

    def test_asserts(self):
        self.assert_model_can_create()
        self.assert_api_post()
