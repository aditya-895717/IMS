from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

admin.site.site_header = "Fortius IMS"
admin.site.site_title = "Fortius Admin"
admin.site.index_title = "Router Refurbishment System"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("", include("apps.reports.dashboard_urls")),
    path("masters/", include("apps.masters.urls", namespace="masters")),
    path("inward/", include("apps.inward.urls", namespace="inward")),
    path("inventory/", include("apps.inventory.urls", namespace="inventory")),
    path("refurbishment/", include("apps.refurbishment.urls", namespace="refurbishment")),
    path("testing/", include("apps.testing_module.urls", namespace="testing")),
    path("repair/", include("apps.repair.urls", namespace="repair")),
    path("qc/", include("apps.qc.urls", namespace="qc")),
    path("packing/", include("apps.packing.urls", namespace="packing")),
    path("dispatch/", include("apps.dispatch.urls", namespace="dispatch")),
    path("reports/", include("apps.reports.urls", namespace="reports")),
    path("api/", include("apps.inventory.api_urls")),
    path("", RedirectView.as_view(url="/dashboard/", permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
