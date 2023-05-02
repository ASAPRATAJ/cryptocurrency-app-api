"""
URL mapping for the vote app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from vote import views


router = DefaultRouter()
router.register('votes', views.VoteViewSet)

app_name = 'vote'

urlpatterns = [
    path('', include(router.urls)),
]