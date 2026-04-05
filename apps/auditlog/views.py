from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import AuditTrail
from apps.accounts.mixins import RoleRequiredMixin, ADMIN_ONLY


class AuditTrailListView(RoleRequiredMixin, ListView):
    allowed_roles = ADMIN_ONLY
    model = AuditTrail
    template_name = "auditlog/list.html"
    context_object_name = "entries"
    paginate_by = 50

    def get_queryset(self):
        return AuditTrail.objects.select_related("user")
