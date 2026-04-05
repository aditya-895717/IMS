from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

ADMIN_ONLY = ["admin"]
ADMIN_INV = ["admin", "inventory_manager"]
ADMIN_INV_SUP = ["admin", "inventory_manager", "production_supervisor"]
ADMIN_TESTING = ["admin", "testing_operator"]
ADMIN_REPAIR = ["admin", "repair_technician"]
ADMIN_QC = ["admin", "qc_inspector"]
ADMIN_DISPATCH = ["admin", "dispatch_executive"]
ALL_ROLES = [
    "admin", "inventory_manager", "production_supervisor",
    "testing_operator", "repair_technician", "qc_inspector",
    "dispatch_executive", "management",
]
REPORT_ROLES = [
    "admin", "inventory_manager", "production_supervisor",
    "dispatch_executive", "management",
]


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        return self.request.user.role in self.allowed_roles

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("accounts:login")
