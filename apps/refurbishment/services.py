from django.db import transaction
from apps.auditlog.utils import log_action

VALID_TRANSITIONS = {
    "RECEIVED": ["SORTING"],
    "SORTING": ["CLEANING"],
    "CLEANING": ["TESTING"],
    "TESTING": ["QC", "REPAIR"],
    "REPAIR": ["RETESTING"],
    "RETESTING": ["QC", "REPAIR", "HOLD", "SCRAP"],
    "QC": ["PACKING", "REPAIR"],
    "PACKING": ["READY"],
    "READY": ["DISPATCHED"],
    "HOLD": ["REPAIR", "SCRAP"],
    "SCRAP": [],
    "DISPATCHED": [],
}


def _validate_transition(from_code, to_code):
    allowed = VALID_TRANSITIONS.get(from_code, [])
    if to_code not in allowed:
        raise ValueError(
            f"Cannot move '{from_code}' → '{to_code}'. "
            f"Allowed: {allowed or ['none — terminal stage']}"
        )


@transaction.atomic
def move_router_stage(router_unit, to_stage_code, moved_by,
                      remarks="", outcome="", ref_type="", ref_id=None):
    # Imports inside function to avoid circular imports
    from apps.masters.models import StageMaster
    from .models import StageMovement

    _validate_transition(router_unit.current_stage.stage_code, to_stage_code)
    to_stage = StageMaster.objects.get(stage_code=to_stage_code)
    old_stage = router_unit.current_stage.stage_name

    StageMovement.objects.create(
        router_unit=router_unit,
        from_stage=router_unit.current_stage,
        to_stage=to_stage,
        moved_by=moved_by,
        remarks=remarks,
        outcome=outcome,
        ref_type=ref_type,
        ref_id=ref_id,
    )
    router_unit.current_stage = to_stage
    router_unit.updated_by = moved_by
    router_unit.save(update_fields=["current_stage", "updated_by", "updated_at"])

    log_action(
        moved_by, "refurbishment", "MOVE", router_unit.pk,
        f"{router_unit.serial_number}: {old_stage} → {to_stage.stage_name}",
    )
    return router_unit
