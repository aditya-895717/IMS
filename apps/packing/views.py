from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from apps.accounts.mixins import RoleRequiredMixin, ADMIN_DISPATCH
from apps.inventory.models import RouterUnit
from apps.refurbishment.services import move_router_stage
from .models import PackingRecord
from .forms import PackingRecordForm


class PackingRecordListView(RoleRequiredMixin, ListView):
    allowed_roles = ADMIN_DISPATCH
    model = PackingRecord
    template_name = "packing/list.html"
    context_object_name = "records"
    paginate_by = 50

    def get_queryset(self):
        return PackingRecord.objects.select_related(
            "router_unit__model", "router_unit__current_stage", "packed_by"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["pending_routers"] = RouterUnit.objects.filter(
            current_stage__stage_code="PACKING", is_active=True
        ).select_related("model", "current_stage")[:50]
        return ctx


class PackingRecordCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ADMIN_DISPATCH
    model = PackingRecord
    form_class = PackingRecordForm
    template_name = "packing/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.router = get_object_or_404(
            RouterUnit.objects.select_related("current_stage"),
            pk=self.kwargs["router_pk"], is_active=True,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["router"] = self.router
        return ctx

    def form_valid(self, form):
        form.instance.router_unit = self.router
        form.instance.packed_by = self.request.user
        response = super().form_valid(form)
        move_router_stage(
            self.router, "READY", self.request.user,
            outcome="pass", ref_type="PackingRecord", ref_id=self.object.pk,
        )
        messages.success(
            self.request,
            f"Packing saved. {self.router.serial_number} moved to Ready Stock.",
        )
        return response

    def get_success_url(self):
        return reverse("packing:list")
