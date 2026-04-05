from django.urls import path
from . import views

app_name = "packing"

urlpatterns = [
    path("list/", views.PackingRecordListView.as_view(), name="list"),
    path("create/<int:router_pk>/", views.PackingRecordCreateView.as_view(), name="create"),
]
