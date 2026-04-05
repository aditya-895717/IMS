from django.contrib import admin
from .models import RouterModel, StageMaster, LocationMaster, SparePart


@admin.register(RouterModel)
class RouterModelAdmin(admin.ModelAdmin):
    list_display = ("model_name", "airtel_model_code", "category", "brand", "is_active")
    list_editable = ("is_active",)
    search_fields = ("model_name", "airtel_model_code")
    list_filter = ("category", "brand", "is_active")


@admin.register(StageMaster)
class StageMasterAdmin(admin.ModelAdmin):
    list_display = ("sequence_no", "stage_code", "stage_name", "is_active")
    list_editable = ("is_active",)
    ordering = ("sequence_no",)


@admin.register(LocationMaster)
class LocationMasterAdmin(admin.ModelAdmin):
    list_display = ("location_code", "location_name", "description")
    search_fields = ("location_code", "location_name")


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = (
        "part_code", "part_name", "current_stock",
        "min_stock", "unit", "is_low_stock", "location",
    )
    search_fields = ("part_code", "part_name")
    list_filter = ("location",)
