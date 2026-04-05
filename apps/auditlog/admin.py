from django.contrib import admin
from .models import AuditTrail


@admin.register(AuditTrail)
class AuditTrailAdmin(admin.ModelAdmin):
    list_display = (
        "action_time", "user", "module_name",
        "action", "object_id", "description",
    )
    list_filter = ("module_name", "action", "action_time")
    search_fields = ("user__username", "description", "object_id")
    readonly_fields = (
        "action_time", "user", "module_name", "action",
        "object_id", "description", "old_data", "new_data", "ip_address",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
