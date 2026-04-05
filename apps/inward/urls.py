from django.urls import path
from . import views

app_name = "inward"

urlpatterns = [
    path("list/", views.InwardListView.as_view(), name="list"),
    path("create/", views.InwardCreateView.as_view(), name="create"),
    path("<int:pk>/", views.InwardDetailView.as_view(), name="detail"),
]
