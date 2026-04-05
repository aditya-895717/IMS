from django.urls import path
from . import views

app_name = "testing"

urlpatterns = [
    path("list/", views.TestRecordListView.as_view(), name="list"),
    path("create/<int:router_pk>/", views.TestRecordCreateView.as_view(), name="create"),
]
