from django.urls import path
from . import views

app_name = "dispatch"

urlpatterns = [
    path("list/", views.DispatchListView.as_view(), name="list"),
    path("create/", views.DispatchCreateView.as_view(), name="create"),
    path("<int:pk>/", views.DispatchDetailView.as_view(), name="detail"),
]
