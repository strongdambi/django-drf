from django.urls import path
from . import views

urlpatterns = [
    path("translate/", views.TranslateAPIView.as_view(), name="translate")
]