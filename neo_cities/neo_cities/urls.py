"""neo_cities URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from neo_api import views

router = routers.DefaultRouter()
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
