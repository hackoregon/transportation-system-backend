import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from api.models import Crash, Partic, Vhcl
from api.serializers import CrashSerializer, ParticSerializer, VhclSerializer


client = Client()

class GetAllCrashesTest(TestCase):
    """ Test module for GET all crashes from API call """

    def setUp(self):
        Crash.objects.create(crash_id=1547419,crash_yr_no=2013)
        
    def test_get_all_crashes(self):
        # get API responses
        response = client.get('/api/crashes/1547419/')
        # get data from db
        crashes = Crash.objects.get(crash_id=1547419)
        serializer = CrashSerializer(crashes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)