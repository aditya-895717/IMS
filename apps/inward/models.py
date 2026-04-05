from django.db import models
from django.conf import settings


class InwardEntry(models.Model):
    inward_no = models.CharField(max_length=30, unique=True)
    inward_date = models.DateField()
    source_name = models.CharField(max_length=200)
    vehicle_no = models.CharField(max_length=30, blank=True)
    challan_no = models.CharField(max_length=50, blank=True)
    remarks = models.TextField(blank=True)
    document = models.FileField(upload_to="inward_docs/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="inward_entries",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.inward_no

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Inward Entries"


class InwardItem(models.Model):
    CONDITION = [("good", "Good"), ("damaged", "Damaged"), ("unknown", "Unknown")]
    inward_entry = models.ForeignKey(
        InwardEntry, related_name="items", on_delete=models.CASCADE
    )
    serial_number = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=20)
    model = models.ForeignKey("masters.RouterModel", on_delete=models.PROTECT)
    initial_condition = models.CharField(max_length=20, choices=CONDITION)
    batch_no = models.CharField(max_length=50, blank=True)
    remarks = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.serial_number

    class Meta:
        ordering = ["serial_number"]
