from django.db import models
from django.conf import settings


class PackingRecord(models.Model):
    router_unit = models.OneToOneField(
        "inventory.RouterUnit", on_delete=models.PROTECT,
        related_name="packing",
    )
    packed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    packed_at = models.DateTimeField(auto_now_add=True)
    box_no = models.CharField(max_length=50)
    remarks = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"Box {self.box_no} — {self.router_unit.serial_number}"

    class Meta:
        ordering = ["-packed_at"]
