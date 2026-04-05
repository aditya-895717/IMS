from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from apps.accounts.mixins import RoleRequiredMixin, ADMIN_INV_SUP
from .models import StageMovement


class StageMovementListView(RoleRequiredMixin, ListView):
    allowed_roles = ADMIN_INV_SUP
    model = StageMovement
    template_name = "refurbishment/list.html"
    context_object_name = "movements"
    paginate_by = 50

    def get_queryset(self):
        return StageMovement.objects.select_related(
            "router_unit", "from_stage", "to_stage", "moved_by"
        )
