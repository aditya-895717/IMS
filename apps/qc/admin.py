from django.contrib import admin
from .models import QCRecord


@admin.register(QCRecord)
class QCRecordAdmin(admin.ModelAdmin):
    list_display = ("router_unit", "inspected_by", "inspected_at", "qc_result")
    list_filter = ("qc_result",)
    search_fields = ("router_unit__serial_number", "rejection_reason")
    readonly_fields = ("inspected_at",)
