import datetime
from django.db import transaction
from apps.auditlog.utils import log_action


def _next_grn():
    from .models import InwardEntry
    y = datetime.date.today().year
    n = InwardEntry.objects.filter(inward_no__startswith=f"GRN-{y}-").count() + 1
    return f"GRN-{y}-{n:04d}"


@transaction.atomic
def create_inward_with_items(inward_data, items_data, created_by):
    from .models import InwardEntry, InwardItem
    from apps.inventory.models import RouterUnit
    from apps.masters.models import StageMaster

    received = StageMaster.objects.get(stage_code="RECEIVED")
    entry = InwardEntry.objects.create(
        inward_no=_next_grn(), created_by=created_by, **inward_data
    )
    for d in items_data:
        sn = d.pop("serial_number", "").strip().upper()
        mac = d.pop("mac_address", "").strip().upper()
        if RouterUnit.objects.filter(serial_number=sn).exists():
            raise ValueError(f"Serial '{sn}' already exists.")
        if RouterUnit.objects.filter(mac_address=mac).exists():
            raise ValueError(f"MAC '{mac}' already exists.")
        item = InwardItem.objects.create(
            inward_entry=entry, serial_number=sn, mac_address=mac, **d
        )
        RouterUnit.objects.create(
            serial_number=sn, mac_address=mac,
            model=item.model, inward_item=item,
            batch_no=item.batch_no, current_stage=received,
            current_status="active",
            created_by=created_by, updated_by=created_by,
        )
    log_action(
        created_by, "inward", "CREATE", entry.pk,
        f"GRN {entry.inward_no}: {len(items_data)} units registered",
    )
    return entry
