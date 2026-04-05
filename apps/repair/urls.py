from django.urls import path
from . import views

app_name = "repair"

urlpatterns = [
    path("list/", views.RepairRecordListView.as_view(), name="list"),
    path("create/<int:router_pk>/", views.RepairRecordCreateView.as_view(), name="create"),
]
