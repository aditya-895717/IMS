from django.contrib import admin
from .models import PackingRecord


@admin.register(PackingRecord)
class PackingRecordAdmin(admin.ModelAdmin):
    list_display = ("router_unit", "packed_by", "packed_at", "box_no")
    search_fields = ("router_unit__serial_number", "box_no")
    readonly_fields = ("packed_at",)
