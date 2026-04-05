from django.contrib import admin
from .models import DispatchEntry, DispatchItem


class DispatchItemInline(admin.TabularInline):
    model = DispatchItem
    extra = 1
    raw_id_fields = ("router_unit",)


@admin.register(DispatchEntry)
class DispatchEntryAdmin(admin.ModelAdmin):
    list_display = (
        "dispatch_no", "dispatch_date", "destination",
        "transporter", "created_by", "created_at",
    )
    list_filter = ("dispatch_date",)
    search_fields = ("dispatch_no", "destination", "challan_no")
    readonly_fields = ("dispatch_no", "created_by", "created_at")
    inlines = [DispatchItemInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
