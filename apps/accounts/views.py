from django.contrib.auth.views import LoginView


ROLE_REDIRECT = {
    "admin": "/dashboard/",
    "inventory_manager": "/dashboard/",
    "production_supervisor": "/dashboard/",
    "testing_operator": "/testing/list/",
    "repair_technician": "/repair/list/",
    "qc_inspector": "/qc/list/",
    "dispatch_executive": "/dispatch/list/",
    "management": "/reports/stock/",
}


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return ROLE_REDIRECT.get(self.request.user.role, "/dashboard/")
