from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from neo_api import views

router = routers.DefaultRouter()
# TODO This can be refactored to be less redundant
router.register(r'events', views.EventViewSet)
router.register(r'resources', views.ResourceViewSet)
router.register(r'threshold', views.ThresholdViewSet)
router.register(r'role', views.RoleViewSet)
router.register(r'resourcesdepot', views.ResourceDepotViewSet)
router.register(r'scenario', views.ScenarioViewSet)
router.register(r'briefing', views.BriefingViewSet)
router.register(r'score', views.ScoreViewSet)
router.register(r'participant', views.ParticipantViewSet)
router.register(r'session', views.SessionViewSet)
router.register(r'action', views.ActionViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    path('admin/', admin.site.urls),
    #   url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
