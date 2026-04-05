from django.urls import path
from . import views

app_name = "qc"

urlpatterns = [
    path("list/", views.QCRecordListView.as_view(), name="list"),
    path("create/<int:router_pk>/", views.QCRecordCreateView.as_view(), name="create"),
]
