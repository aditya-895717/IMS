from django.db import models
from django.conf import settings


class RepairRecord(models.Model):
    STATUS = [
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("beyond_repair", "Beyond Repair"),
    ]
    router_unit = models.ForeignKey(
        "inventory.RouterUnit", related_name="repairs",
        on_delete=models.PROTECT,
    )
    repaired_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    repair_date = models.DateField()
    issue_type = models.CharField(max_length=100)
    diagnosis = models.TextField()
    action_taken = models.TextField()
    repair_status = models.CharField(
        max_length=20, choices=STATUS, default="in_progress"
    )
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Repair {self.pk} — {self.router_unit.serial_number}"

    class Meta:
        ordering = ["-repair_date"]


class RepairPartUsage(models.Model):
    repair_record = models.ForeignKey(
        RepairRecord, related_name="parts_used", on_delete=models.CASCADE
    )
    spare_part = models.ForeignKey("masters.SparePart", on_delete=models.PROTECT)
    qty_used = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        from django.db.models import F
        from django.db import transaction

        with transaction.atomic():
            super().save(*args, **kwargs)
            type(self.spare_part).objects.filter(
                pk=self.spare_part.pk
            ).update(current_stock=F("current_stock") - self.qty_used)

    def __str__(self):
        return f"{self.qty_used}x {self.spare_part.part_name}"

    class Meta:
        ordering = ["pk"]
