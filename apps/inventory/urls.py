from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("list/", views.RouterUnitListView.as_view(), name="list"),
    path("<int:pk>/", views.RouterUnitDetailView.as_view(), name="detail"),
]
