from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from neo_api import views

router = routers.DefaultRouter()
# TODO This can be refactored to be less redundant
router.register(r'event', views.EventViewSet)
router.register(r'resource', views.ResourceViewSet)
router.register(r'threshold', views.ThresholdViewSet)
router.register(r'role', views.RoleViewSet)
router.register(r'message', views.MessageViewSet)
router.register(r'resourcesdepot', views.ResourceDepotViewSet)
router.register(r'scenario', views.ScenarioViewSet)
router.register(r'score', views.ScoreViewSet)
router.register(r'participant', views.ParticipantViewSet)
router.register(r'session', views.SessionViewSet)
router.register(r'action', views.ActionViewSet)

urlpatterns = [
    # url(r'^initParticipant/{pk}/', views.InitParticipant),
    path('api/resourceeventstate/<sessionKey>', views.ResourceEventStateViewSet.as_view()),
    path('api/briefings/<sessionKey>', views.BriefingItemView.as_view()),
    path('api/events/<sessionKey>', views.EventItemView.as_view()),
    path('api/messages/<chatSessionId>', views.MessageItemView.as_view()),
    path('api/resources/<sessionKey>', views.ResourceItemView.as_view()),
    path('api/initparticipant/<participantKey>', views.InitParticipant.as_view()),
    path('api/startsimulation/<sessionKey>', views.StartSimulation.as_view()),
    url(r'^api/', include(router.urls)),
    path('admin/', admin.site.urls),
    #   url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
