from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Crash, Partic, Vhcl
from api.serializers import CrashSerializer, ParticSerializer, VhclSerializer

class CrashTests(APITestCase):
    
    def setUp(self):
        Crash.objects.create(crash_id=431213)

    def test_crash_serializer(self):
        """
        Ensure that serializer data matches the response data
        """
        response = self.client.get('/api/crashes/431213/')
        crash = Crash.objects.get(crash_id=431213)
        serializer = CrashSerializer(crash)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_crash_permissions(self):
        """
        Ensure that unauthenticated users cannot create new records
        """
        response = self.client.post('/api/crashes/', {'crash_id':123451221}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Crash.objects.count(), 1)
        self.assertNotEqual(Crash.objects.get().crash_id, 123451221)

class ParticTests(APITestCase):
    
    def setUp(self):
        Partic.objects.create(partic_id=112211)

    def test_partic_serializer(self):
        """
        Ensure that serializer data matches the response data
        """
        response = self.client.get('/api/participants/112211/')
        partic = Partic.objects.get(partic_id=112211)
        serializer = ParticSerializer(partic)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class VhclTests(APITestCase):
    
    def setUp(self):
        Vhcl.objects.create(vhcl_id=2121444)

    def test_vhcl_serializer(self):
        """
        Ensure that serializer data matches the response data
        """
        response = self.client.get('/api/vehicles/2121444/')
        vhcl = Vhcl.objects.get(vhcl_id=2121444)
        serializer = VhclSerializer(vhcl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)