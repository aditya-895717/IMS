from django.db import models
from django.conf import settings


class TestRecord(models.Model):
    RESULT = [("pass", "Pass"), ("fail", "Fail")]
    router_unit = models.ForeignKey(
        "inventory.RouterUnit", related_name="tests",
        on_delete=models.PROTECT,
    )
    tested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    tested_at = models.DateTimeField(auto_now_add=True)
    is_retest = models.BooleanField(default=False)
    power_ok = models.BooleanField(default=False)
    boot_ok = models.BooleanField(default=False)
    wifi_ok = models.BooleanField(default=False)
    lan_ok = models.BooleanField(default=False)
    led_ok = models.BooleanField(default=False)
    adapter_ok = models.BooleanField(default=False)
    firmware_ok = models.BooleanField(default=False)
    reset_button_ok = models.BooleanField(default=False)
    overall_result = models.CharField(max_length=10, choices=RESULT)
    fail_reason = models.CharField(max_length=300, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Test {self.pk} — {self.router_unit.serial_number} — {self.overall_result}"

    class Meta:
        ordering = ["-tested_at"]
