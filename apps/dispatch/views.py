from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db import transaction
from apps.accounts.mixins import RoleRequiredMixin, ADMIN_DISPATCH
from apps.inventory.models import RouterUnit
from apps.refurbishment.services import move_router_stage
from .models import DispatchEntry, DispatchItem
from .forms import DispatchEntryForm
from .services import create_dispatch_with_items


class DispatchListView(RoleRequiredMixin, ListView):
    allowed_roles = ADMIN_DISPATCH
    model = DispatchEntry
    template_name = "dispatch/list.html"
    context_object_name = "entries"
    paginate_by = 50

    def get_queryset(self):
        return DispatchEntry.objects.select_related("created_by").prefetch_related(
            "items__router_unit"
        )


class DispatchDetailView(RoleRequiredMixin, DetailView):
    allowed_roles = ADMIN_DISPATCH
    model = DispatchEntry
    template_name = "dispatch/detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        return DispatchEntry.objects.select_related("created_by").prefetch_related(
            "items__router_unit__model"
        )


class DispatchCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ADMIN_DISPATCH
    model = DispatchEntry
    form_class = DispatchEntryForm
    template_name = "dispatch/create.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["ready_routers"] = RouterUnit.objects.filter(
            current_stage__stage_code="READY", is_active=True
        ).select_related("model")[:100]
        return ctx

    def form_valid(self, form):
        selected_ids = self.request.POST.getlist("router_ids")
        if not selected_ids:
            form.add_error(None, "Please select at least one router for dispatch.")
            return self.form_invalid(form)

        routers = RouterUnit.objects.filter(
            pk__in=selected_ids, current_stage__stage_code="READY", is_active=True
        ).select_related("current_stage")

        if routers.count() != len(selected_ids):
            form.add_error(None, "Some selected routers are no longer available.")
            return self.form_invalid(form)

        try:
            dispatch_data = {
                "dispatch_date": form.cleaned_data["dispatch_date"],
                "destination": form.cleaned_data["destination"],
                "transporter": form.cleaned_data["transporter"],
                "vehicle_no": form.cleaned_data["vehicle_no"],
                "challan_no": form.cleaned_data["challan_no"],
                "remarks": form.cleaned_data["remarks"],
            }
            entry = create_dispatch_with_items(
                dispatch_data, list(routers), self.request.user
            )
            messages.success(
                self.request,
                f"Dispatch {entry.dispatch_no} created with {routers.count()} units.",
            )
            return super().form_valid(form)
        except ValueError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("dispatch:list")
