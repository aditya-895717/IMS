from django.contrib import admin
from .models import RouterUnit


@admin.register(RouterUnit)
class RouterUnitAdmin(admin.ModelAdmin):
    list_display = (
        "serial_number", "mac_address", "model", "current_stage",
        "current_status", "current_location", "is_active", "created_at",
    )
    list_filter = ("current_stage", "current_status", "model", "is_active")
    search_fields = ("serial_number", "mac_address", "batch_no")
    list_editable = ("current_status", "is_active")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by", "inward_item")
