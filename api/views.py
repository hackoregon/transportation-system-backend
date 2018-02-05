from api.models import Crash, Partic, Vhcl
from rest_framework.decorators import api_view, detail_route
from api.serializers import CrashSerializer, ParticSerializer, VhclSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets

class CrashViewSet(viewsets.ModelViewSet):
    
    queryset = Crash.objects.all()
    serializer_class = CrashSerializer

class ParticViewSet(viewsets.ModelViewSet):

    queryset = Partic.objects.all()
    serializer_class = ParticSerializer

class VhclViewSet(viewsets.ModelViewSet):

    queryset = Vhcl.objects.all()
    serializer_class = VhclSerializer
