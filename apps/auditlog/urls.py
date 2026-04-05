from django.urls import path
from . import views

app_name = "auditlog"

urlpatterns = [
    path("list/", views.AuditTrailListView.as_view(), name="list"),
]
