from django.urls import include
from django.urls import path
from django.views.generic.base import RedirectView
from rest_framework import routers

from .viewsets import company
from .viewsets import summary

router = routers.DefaultRouter(trailing_slash=False)
router.register("company", company.ViewSet, basename="company")
router.register("summary", summary.ViewSet, basename="summary")

urlpatterns = [
  path("", RedirectView.as_view(pattern_name="api-root", permanent=False)),
  path("api/", include(router.urls)),
]
