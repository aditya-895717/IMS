from django.urls import path
from . import views

app_name = "masters"

urlpatterns = [
    path("models/", views.RouterModelListView.as_view(), name="router_model_list"),
    path("models/add/", views.RouterModelCreateView.as_view(), name="router_model_add"),
    path("models/<int:pk>/edit/", views.RouterModelUpdateView.as_view(), name="router_model_edit"),
    path("spares/", views.SparePartListView.as_view(), name="spare_part_list"),
    path("spares/add/", views.SparePartCreateView.as_view(), name="spare_part_add"),
    path("spares/<int:pk>/edit/", views.SparePartUpdateView.as_view(), name="spare_part_edit"),
    path("locations/", views.LocationListView.as_view(), name="location_list"),
    path("locations/add/", views.LocationCreateView.as_view(), name="location_add"),
]
