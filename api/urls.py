from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import views
from rest_framework.schemas import get_schema_view


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'crashes', views.CrashViewSet)
router.register(r'participants', views.ParticViewSet)
router.register(r'vehicles', views.VhclViewSet)

#schema view
schema_view = get_schema_view(title='ODOT Crash API')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^schema/$', schema_view),
    url(r'^api/', include(router.urls)),
]