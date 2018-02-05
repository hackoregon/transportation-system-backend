from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import views
from rest_framework.schemas import get_schema_view


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'api', views.CrashViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls)),
]