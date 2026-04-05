from django.contrib import admin
from .models import RepairRecord, RepairPartUsage


class RepairPartUsageInline(admin.TabularInline):
    model = RepairPartUsage
    extra = 1


@admin.register(RepairRecord)
class RepairRecordAdmin(admin.ModelAdmin):
    list_display = (
        "router_unit", "repaired_by", "repair_date",
        "repair_status", "issue_type",
    )
    list_filter = ("repair_status", "repair_date")
    search_fields = ("router_unit__serial_number", "issue_type")
    inlines = [RepairPartUsageInline]
