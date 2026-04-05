from django.db import models
from django.conf import settings


class RouterUnit(models.Model):
    STATUS = [
        ("active", "Active"),
        ("hold", "On Hold"),
        ("scrap", "Scrapped"),
        ("dispatched", "Dispatched"),
    ]
    serial_number = models.CharField(max_length=100, unique=True, db_index=True)
    mac_address = models.CharField(max_length=20, unique=True, db_index=True)
    model = models.ForeignKey("masters.RouterModel", on_delete=models.PROTECT)
    inward_item = models.OneToOneField("inward.InwardItem", on_delete=models.PROTECT)
    batch_no = models.CharField(max_length=50, blank=True)
    current_stage = models.ForeignKey(
        "masters.StageMaster", on_delete=models.PROTECT,
        related_name="router_units",
    )
    current_status = models.CharField(max_length=20, choices=STATUS, default="active")
    current_location = models.ForeignKey(
        "masters.LocationMaster", null=True, blank=True, on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="created_units",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="updated_units", null=True, blank=True,
    )

    def __str__(self):
        return f"{self.serial_number} | {self.model} | {self.current_stage.stage_code}"

    class Meta:
        ordering = ["-created_at"]
