from django.urls import path
from . import views

app_name = "refurbishment"

urlpatterns = [
    path("list/", views.StageMovementListView.as_view(), name="list"),
]
