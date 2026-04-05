import datetime
from django.db import transaction
from apps.auditlog.utils import log_action


def _next_dis():
    from .models import DispatchEntry
    y = datetime.date.today().year
    n = DispatchEntry.objects.filter(dispatch_no__startswith=f"DIS-{y}-").count() + 1
    return f"DIS-{y}-{n:04d}"


@transaction.atomic
def create_dispatch_with_items(dispatch_data, router_units, created_by):
    from .models import DispatchEntry, DispatchItem
    from apps.refurbishment.services import move_router_stage

    entry = DispatchEntry.objects.create(
        dispatch_no=_next_dis(), created_by=created_by, **dispatch_data
    )
    for ru in router_units:
        DispatchItem.objects.create(dispatch_entry=entry, router_unit=ru)
        move_router_stage(
            ru, "DISPATCHED", created_by,
            remarks=f"Dispatched via {entry.dispatch_no}",
            outcome="pass", ref_type="DispatchEntry", ref_id=entry.pk,
        )
    log_action(
        created_by, "dispatch", "CREATE", entry.pk,
        f"Dispatch {entry.dispatch_no}: {len(router_units)} units dispatched",
    )
    return entry
