from django.db import models


class RouterModel(models.Model):
    model_name = models.CharField(max_length=100, unique=True)
    airtel_model_code = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, default="Airtel")
    specifications = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.model_name

    class Meta:
        ordering = ["model_name"]


class StageMaster(models.Model):
    stage_code = models.CharField(max_length=20, unique=True)
    stage_name = models.CharField(max_length=100)
    sequence_no = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sequence_no}. {self.stage_name}"

    class Meta:
        ordering = ["sequence_no"]


class LocationMaster(models.Model):
    location_code = models.CharField(max_length=20, unique=True)
    location_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.location_name

    class Meta:
        ordering = ["location_name"]


class SparePart(models.Model):
    part_code = models.CharField(max_length=30, unique=True)
    part_name = models.CharField(max_length=150)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_stock = models.DecimalField(max_digits=10, decimal_places=2, default=5)
    unit = models.CharField(max_length=20)
    location = models.ForeignKey(
        "LocationMaster", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.part_code} — {self.part_name}"

    @property
    def is_low_stock(self):
        return self.current_stock <= self.min_stock

    class Meta:
        ordering = ["part_name"]
