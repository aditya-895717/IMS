from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from apps.accounts.mixins import RoleRequiredMixin, ADMIN_TESTING
from apps.inventory.models import RouterUnit
from apps.refurbishment.services import move_router_stage
from .models import TestRecord
from .forms import TestRecordForm


class TestRecordListView(RoleRequiredMixin, ListView):
    allowed_roles = ADMIN_TESTING
    model = TestRecord
    template_name = "testing_module/list.html"
    context_object_name = "records"
    paginate_by = 50

    def get_queryset(self):
        return TestRecord.objects.select_related(
            "router_unit__model", "router_unit__current_stage", "tested_by"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["pending_routers"] = RouterUnit.objects.filter(
            current_stage__stage_code__in=["TESTING", "RETESTING"], is_active=True
        ).select_related("model", "current_stage")[:50]
        return ctx


class TestRecordCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ADMIN_TESTING
    model = TestRecord
    form_class = TestRecordForm
    template_name = "testing_module/create.html"

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
        form.instance.tested_by = self.request.user
        form.instance.is_retest = (
            self.router.current_stage.stage_code == "RETESTING"
        )
        response = super().form_valid(form)
        result = form.instance.overall_result
        next_stage = "QC" if result == "pass" else "REPAIR"
        move_router_stage(
            self.router, next_stage, self.request.user,
            outcome=result, ref_type="TestRecord", ref_id=self.object.pk,
        )
        messages.success(
            self.request,
            f"Test saved. {self.router.serial_number} moved to {next_stage}.",
        )
        return response

    def get_success_url(self):
        return reverse("testing:list")
