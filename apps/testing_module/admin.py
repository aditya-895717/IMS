from django.contrib import admin
from .models import TestRecord


@admin.register(TestRecord)
class TestRecordAdmin(admin.ModelAdmin):
    list_display = (
        "router_unit", "tested_by", "tested_at",
        "is_retest", "overall_result",
    )
    list_filter = ("overall_result", "is_retest", "tested_at")
    search_fields = ("router_unit__serial_number",)
    readonly_fields = ("tested_at",)
