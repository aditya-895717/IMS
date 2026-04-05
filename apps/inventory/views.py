from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from apps.accounts.mixins import RoleRequiredMixin, ALL_ROLES
from .models import RouterUnit
from .forms import RouterSearchForm


class RouterUnitListView(RoleRequiredMixin, ListView):
    allowed_roles = ALL_ROLES
    model = RouterUnit
    template_name = "inventory/list.html"
    context_object_name = "routers"
    paginate_by = 50

    def get_queryset(self):
        qs = RouterUnit.objects.select_related(
            "model", "current_stage", "current_location", "created_by"
        ).filter(is_active=True)
        serial = self.request.GET.get("serial", "").strip()
        stage = self.request.GET.get("stage", "").strip()
        status = self.request.GET.get("status", "").strip()
        if serial:
            qs = qs.filter(serial_number__icontains=serial)
        if stage:
            qs = qs.filter(current_stage__stage_code=stage)
        if status:
            qs = qs.filter(current_status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_form"] = RouterSearchForm(self.request.GET)
        return ctx


class RouterUnitDetailView(RoleRequiredMixin, DetailView):
    allowed_roles = ALL_ROLES
    model = RouterUnit
    template_name = "inventory/detail.html"
    context_object_name = "router"

    def get_queryset(self):
        return RouterUnit.objects.select_related(
            "model", "current_stage", "current_location",
            "inward_item__inward_entry", "created_by", "updated_by",
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["movements"] = self.object.movements.select_related(
            "from_stage", "to_stage", "moved_by"
        )[:20]
        ctx["tests"] = self.object.tests.select_related("tested_by")[:10]
        ctx["repairs"] = self.object.repairs.select_related("repaired_by")[:10]
        ctx["qc_checks"] = self.object.qc_checks.select_related("inspected_by")[:10]
        return ctx
