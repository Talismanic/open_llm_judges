from django.urls import path
from .views import JudgeAPIView, ArchetypeListAPIView

urlpatterns = [
    path("judge/", JudgeAPIView.as_view(), name="judge-api"),
    path("archetypes/", ArchetypeListAPIView.as_view(), name="archetypes-api"),
]
