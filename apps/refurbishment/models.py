from django.db import models
from django.conf import settings


class StageMovement(models.Model):
    OUTCOME = [("pass", "Pass"), ("fail", "Fail"), ("rework", "Rework"), ("", "—")]
    router_unit = models.ForeignKey(
        "inventory.RouterUnit", related_name="movements",
        on_delete=models.PROTECT,
    )
    from_stage = models.ForeignKey(
        "masters.StageMaster", related_name="outgoing",
        on_delete=models.PROTECT, null=True, blank=True,
    )
    to_stage = models.ForeignKey(
        "masters.StageMaster", related_name="incoming",
        on_delete=models.PROTECT,
    )
    moved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    moved_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    outcome = models.CharField(max_length=20, choices=OUTCOME, blank=True)
    ref_type = models.CharField(max_length=30, blank=True)
    ref_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.router_unit.serial_number}: "
            f"{self.from_stage} → {self.to_stage}"
        )

    class Meta:
        ordering = ["-moved_at"]
