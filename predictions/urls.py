from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PredictionViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'predictions', PredictionViewSet)
router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
