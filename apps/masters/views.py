from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.accounts.mixins import RoleRequiredMixin, ADMIN_INV
from .models import RouterModel, SparePart, LocationMaster
from .forms import RouterModelForm, SparePartForm, LocationMasterForm


class RouterModelListView(RoleRequiredMixin, ListView):
    allowed_roles = ADMIN_INV
    model = RouterModel
    template_name = "masters/router_model_list.html"
    context_object_name = "models"
    paginate_by = 50


class RouterModelCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ADMIN_INV
    model = RouterModel
    form_class = RouterModelForm
    template_name = "masters/router_model_form.html"
    success_url = reverse_lazy("masters:router_model_list")

    def form_valid(self, form):
        messages.success(self.request, "Router model created successfully.")
        return super().form_valid(form)


class RouterModelUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ADMIN_INV
    model = RouterModel
    form_class = RouterModelForm
    template_name = "masters/router_model_form.html"
    success_url = reverse_lazy("masters:router_model_list")

    def form_valid(self, form):
        messages.success(self.request, "Router model updated successfully.")
        return super().form_valid(form)


class SparePartListView(RoleRequiredMixin, ListView):
    allowed_roles = ADMIN_INV
    model = SparePart
    template_name = "masters/spare_part_list.html"
    context_object_name = "parts"
    paginate_by = 50

    def get_queryset(self):
        return SparePart.objects.select_related("location")


class SparePartCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ADMIN_INV
    model = SparePart
    form_class = SparePartForm
    template_name = "masters/spare_part_form.html"
    success_url = reverse_lazy("masters:spare_part_list")

    def form_valid(self, form):
        messages.success(self.request, "Spare part created successfully.")
        return super().form_valid(form)


class SparePartUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = ADMIN_INV
    model = SparePart
    form_class = SparePartForm
    template_name = "masters/spare_part_form.html"
    success_url = reverse_lazy("masters:spare_part_list")

    def form_valid(self, form):
        messages.success(self.request, "Spare part updated successfully.")
        return super().form_valid(form)


class LocationListView(RoleRequiredMixin, ListView):
    allowed_roles = ADMIN_INV
    model = LocationMaster
    template_name = "masters/location_list.html"
    context_object_name = "locations"
    paginate_by = 50


class LocationCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ADMIN_INV
    model = LocationMaster
    form_class = LocationMasterForm
    template_name = "masters/location_form.html"
    success_url = reverse_lazy("masters:location_list")

    def form_valid(self, form):
        messages.success(self.request, "Location created successfully.")
        return super().form_valid(form)
