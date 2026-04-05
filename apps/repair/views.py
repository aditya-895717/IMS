from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from apps.accounts.mixins import RoleRequiredMixin, ADMIN_REPAIR
from apps.inventory.models import RouterUnit
from apps.refurbishment.services import move_router_stage
from .models import RepairRecord
from .forms import RepairRecordForm, RepairPartFormSet


class RepairRecordListView(RoleRequiredMixin, ListView):
    allowed_roles = ADMIN_REPAIR
    model = RepairRecord
    template_name = "repair/list.html"
    context_object_name = "records"
    paginate_by = 50

    def get_queryset(self):
        return RepairRecord.objects.select_related(
            "router_unit__model", "router_unit__current_stage", "repaired_by"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["pending_routers"] = RouterUnit.objects.filter(
            current_stage__stage_code="REPAIR", is_active=True
        ).select_related("model", "current_stage")[:50]
        return ctx


class RepairRecordCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ADMIN_REPAIR
    model = RepairRecord
    form_class = RepairRecordForm
    template_name = "repair/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.router = get_object_or_404(
            RouterUnit.objects.select_related("current_stage"),
            pk=self.kwargs["router_pk"], is_active=True,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["router"] = self.router
        if self.request.POST:
            ctx["part_formset"] = RepairPartFormSet(self.request.POST)
        else:
            ctx["part_formset"] = RepairPartFormSet()
        return ctx

    def form_valid(self, form):
        form.instance.router_unit = self.router
        form.instance.repaired_by = self.request.user
        ctx = self.get_context_data()
        part_formset = ctx["part_formset"]

        response = super().form_valid(form)

        if part_formset.is_valid():
            part_formset.instance = self.object
            part_formset.save()

        status = form.instance.repair_status
        if status == "completed":
            next_stage = "RETESTING"
        elif status == "beyond_repair":
            next_stage = "SCRAP"
            self.router.current_status = "scrap"
            self.router.save(update_fields=["current_status"])
        else:
            messages.success(self.request, f"Repair record saved for {self.router.serial_number}.")
            return response

        move_router_stage(
            self.router, next_stage, self.request.user,
            outcome=status, ref_type="RepairRecord", ref_id=self.object.pk,
        )
        messages.success(
            self.request,
            f"Repair saved. {self.router.serial_number} moved to {next_stage}.",
        )
        return response

    def get_success_url(self):
        return reverse("repair:list")
