from api.models import Crash
from rest_framework.decorators import api_view, detail_route
from api.serializers import CrashSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets

class CrashViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Crash.objects.all()
    serializer_class = CrashSerializer