from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from .models import RouterUnit
from apps.refurbishment.services import VALID_TRANSITIONS
from apps.masters.models import StageMaster


@login_required
@require_GET
def check_serial(request):
    serial = request.GET.get("serial", "").strip().upper()
    if not serial:
        return JsonResponse({"error": "serial required"}, status=400)
    try:
        r = RouterUnit.objects.select_related("model", "current_stage").get(
            serial_number=serial
        )
        return JsonResponse({
            "exists": True,
            "router": {
                "id": r.pk,
                "model": str(r.model),
                "stage": r.current_stage.stage_name,
                "status": r.current_status,
            },
        })
    except RouterUnit.DoesNotExist:
        return JsonResponse({"exists": False, "router": None})


@login_required
@require_GET
def router_details(request):
    serial = request.GET.get("serial", "").strip().upper()
    if not serial:
        return JsonResponse({"error": "serial required"}, status=400)
    try:
        r = RouterUnit.objects.select_related(
            "model", "current_stage", "current_location"
        ).get(serial_number=serial, is_active=True)
        codes = VALID_TRANSITIONS.get(r.current_stage.stage_code, [])
        stages = list(
            StageMaster.objects.filter(stage_code__in=codes).values(
                "stage_code", "stage_name"
            )
        )
        return JsonResponse({
            "id": r.pk,
            "serial": r.serial_number,
            "mac": r.mac_address,
            "model": str(r.model),
            "batch": r.batch_no,
            "current_stage": r.current_stage.stage_name,
            "stage_code": r.current_stage.stage_code,
            "status": r.current_status,
            "location": str(r.current_location) if r.current_location else "—",
            "allowed_next": stages,
        })
    except RouterUnit.DoesNotExist:
        return JsonResponse(
            {"error": f"Router '{serial}' not found."}, status=404
        )
