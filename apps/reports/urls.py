from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("stock/", views.stock_report, name="stock_report"),
]
