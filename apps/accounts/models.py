from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = [
        ("admin", "Admin"),
        ("inventory_manager", "Inventory Manager"),
        ("production_supervisor", "Production Supervisor"),
        ("testing_operator", "Testing Operator"),
        ("repair_technician", "Repair Technician"),
        ("qc_inspector", "QC Inspector"),
        ("dispatch_executive", "Dispatch Executive"),
        ("management", "Management Viewer"),
    ]
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=50, choices=ROLES, default="management")
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} [{self.get_role_display()}]"
