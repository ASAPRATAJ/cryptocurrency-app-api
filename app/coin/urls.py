"""
URL mapping for the coin app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from coin import views


router = DefaultRouter()
router.register('coins', views.CoinViewSet)

app_name = 'coin'

urlpatterns = [
    path('', include(router.urls)),
]
