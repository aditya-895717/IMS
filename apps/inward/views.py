from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from apps.accounts.mixins import RoleRequiredMixin, ADMIN_INV
from .models import InwardEntry, InwardItem
from .forms import InwardEntryForm, InwardItemFormSet
from .services import create_inward_with_items


class InwardListView(RoleRequiredMixin, ListView):
    allowed_roles = ADMIN_INV
    model = InwardEntry
    template_name = "inward/list.html"
    context_object_name = "entries"
    paginate_by = 50

    def get_queryset(self):
        return InwardEntry.objects.select_related("created_by").prefetch_related("items")


class InwardDetailView(RoleRequiredMixin, DetailView):
    allowed_roles = ADMIN_INV
    model = InwardEntry
    template_name = "inward/detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        return InwardEntry.objects.select_related("created_by").prefetch_related(
            "items__model"
        )


class InwardCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ADMIN_INV
    model = InwardEntry
    form_class = InwardEntryForm
    template_name = "inward/create.html"
    success_url = reverse_lazy("inward:list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["formset"] = InwardItemFormSet(self.request.POST, self.request.FILES)
        else:
            ctx["formset"] = InwardItemFormSet()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        formset = ctx["formset"]
        if not formset.is_valid():
            return self.form_invalid(form)
        try:
            inward_data = {
                "inward_date": form.cleaned_data["inward_date"],
                "source_name": form.cleaned_data["source_name"],
                "vehicle_no": form.cleaned_data["vehicle_no"],
                "challan_no": form.cleaned_data["challan_no"],
                "remarks": form.cleaned_data["remarks"],
            }
            if form.cleaned_data.get("document"):
                inward_data["document"] = form.cleaned_data["document"]

            items_data = []
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get("DELETE"):
                    items_data.append({
                        "serial_number": item_form.cleaned_data["serial_number"],
                        "mac_address": item_form.cleaned_data["mac_address"],
                        "model": item_form.cleaned_data["model"],
                        "initial_condition": item_form.cleaned_data["initial_condition"],
                        "batch_no": item_form.cleaned_data.get("batch_no", ""),
                        "remarks": item_form.cleaned_data.get("remarks", ""),
                    })

            entry = create_inward_with_items(inward_data, items_data, self.request.user)
            messages.success(
                self.request,
                f"GRN {entry.inward_no} created with {len(items_data)} units.",
            )
            return super().form_valid(form)
        except ValueError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("inward:list")
