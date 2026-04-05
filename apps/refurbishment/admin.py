from django.contrib import admin
from .models import StageMovement


@admin.register(StageMovement)
class StageMovementAdmin(admin.ModelAdmin):
    list_display = (
        "router_unit", "from_stage", "to_stage",
        "moved_by", "moved_at", "outcome",
    )
    list_filter = ("from_stage", "to_stage", "outcome")
    search_fields = ("router_unit__serial_number",)
    readonly_fields = (
        "router_unit", "from_stage", "to_stage",
        "moved_by", "moved_at", "remarks", "outcome", "ref_type", "ref_id",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
