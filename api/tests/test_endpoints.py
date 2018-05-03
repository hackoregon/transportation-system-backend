from django.test import TestCase
from api.models import Crash, Partic, Vhcl
from rest_framework.test import APIClient, RequestsClient

class CrashTest(TestCase):
    """ Test for Crash model """

    def setUp(self):
        pass

class CrashEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_list_200_response(self):
        response = self.client.get('/api/crashes/')
        assert response.status_code == 200

class ParticTest(TestCase):
    """ Test for Participant model """

    def setUp(self):
        pass

class ParticEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_list_200_response(self):
        response = self.client.get('/api/participants/')
        assert response.status_code == 200
