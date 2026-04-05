from django.db import models
from django.conf import settings


class DispatchEntry(models.Model):
    dispatch_no = models.CharField(max_length=30, unique=True)
    dispatch_date = models.DateField()
    destination = models.CharField(max_length=200)
    transporter = models.CharField(max_length=100)
    vehicle_no = models.CharField(max_length=30, blank=True)
    challan_no = models.CharField(max_length=50, blank=True)
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dispatch_no

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Dispatch Entries"


class DispatchItem(models.Model):
    dispatch_entry = models.ForeignKey(
        DispatchEntry, related_name="items", on_delete=models.CASCADE
    )
    router_unit = models.OneToOneField(
        "inventory.RouterUnit", on_delete=models.PROTECT,
        related_name="dispatch_item",
    )

    def __str__(self):
        return f"{self.dispatch_entry} — {self.router_unit.serial_number}"

    class Meta:
        ordering = ["pk"]
