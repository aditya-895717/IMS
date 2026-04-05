from django.db import models
from django.conf import settings


class QCRecord(models.Model):
    RESULT = [("pass", "Pass"), ("fail", "Fail")]
    router_unit = models.ForeignKey(
        "inventory.RouterUnit", related_name="qc_checks",
        on_delete=models.PROTECT,
    )
    inspected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    inspected_at = models.DateTimeField(auto_now_add=True)
    body_condition = models.BooleanField(default=False)
    serial_verified = models.BooleanField(default=False)
    mac_verified = models.BooleanField(default=False)
    performance_ok = models.BooleanField(default=False)
    ports_ok = models.BooleanField(default=False)
    label_ok = models.BooleanField(default=False)
    qc_result = models.CharField(max_length=10, choices=RESULT)
    rejection_reason = models.CharField(max_length=300, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"QC {self.pk} — {self.router_unit.serial_number} — {self.qc_result}"

    class Meta:
        ordering = ["-inspected_at"]
