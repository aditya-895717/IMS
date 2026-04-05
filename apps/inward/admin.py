from django.contrib import admin
from .models import InwardEntry, InwardItem


class InwardItemInline(admin.TabularInline):
    model = InwardItem
    extra = 1
    fields = ("serial_number", "mac_address", "model", "initial_condition", "batch_no")


@admin.register(InwardEntry)
class InwardEntryAdmin(admin.ModelAdmin):
    list_display = (
        "inward_no", "inward_date", "source_name",
        "created_by", "created_at", "is_active",
    )
    list_filter = ("inward_date", "is_active")
    search_fields = ("inward_no", "source_name", "challan_no")
    readonly_fields = ("inward_no", "created_by", "created_at")
    inlines = [InwardItemInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(InwardItem)
class InwardItemAdmin(admin.ModelAdmin):
    list_display = (
        "serial_number", "mac_address", "model",
        "initial_condition", "inward_entry",
    )
    search_fields = ("serial_number", "mac_address")
    list_filter = ("model", "initial_condition")
