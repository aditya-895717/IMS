from .models import AuditTrail


def log_action(user, module, action, object_id, description,
               old_data=None, new_data=None, request=None):
    ip = None
    if request:
        xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
        ip = xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR")
    AuditTrail.objects.create(
        user=user,
        module_name=module,
        action=action,
        object_id=str(object_id),
        description=description,
        old_data=old_data,
        new_data=new_data,
        ip_address=ip,
    )
