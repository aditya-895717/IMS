from django.urls import path
from . import api_views

urlpatterns = [
    path("check-serial/", api_views.check_serial, name="api_check_serial"),
    path("router-details/", api_views.router_details, name="api_router_details"),
]
