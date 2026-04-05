from django.db import models
from django.conf import settings


class AuditTrail(models.Model):
    ACTIONS = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("MOVE", "Move"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    module_name = models.CharField(max_length=50)
    action = models.CharField(max_length=20, choices=ACTIONS)
    object_id = models.CharField(max_length=50)
    description = models.TextField()
    old_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)
    action_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.action_time} [{self.action}] {self.module_name}"

    class Meta:
        ordering = ["-action_time"]
