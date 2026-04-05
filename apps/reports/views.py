import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.db.models import Count, F
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.inventory.models import RouterUnit
from apps.inward.models import InwardEntry
from apps.dispatch.models import DispatchEntry
from apps.masters.models import SparePart
from apps.auditlog.models import AuditTrail


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "reports/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.now().date()
        sc = dict(
            RouterUnit.objects.filter(is_active=True)
            .values_list("current_stage__stage_code")
            .annotate(c=Count("id"))
        )
        chart = dict(
            RouterUnit.objects.filter(is_active=True)
            .values_list("current_stage__stage_name")
            .annotate(c=Count("id"))
        )
        ctx.update({
            "inward_today": InwardEntry.objects.filter(inward_date=today).count(),
            "in_testing": sc.get("TESTING", 0),
            "in_repair": sc.get("REPAIR", 0),
            "in_qc": sc.get("QC", 0),
            "ready_stock": sc.get("READY", 0),
            "dispatched_today": DispatchEntry.objects.filter(
                dispatch_date=today
            ).count(),
            "low_spare_parts": SparePart.objects.filter(
                current_stock__lte=F("min_stock")
            ).count(),
            "stage_chart_json": json.dumps(chart),
            "total_active": RouterUnit.objects.filter(is_active=True).count(),
            "in_sorting": sc.get("SORTING", 0),
            "in_cleaning": sc.get("CLEANING", 0),
            "in_packing": sc.get("PACKING", 0),
            "recent_audit": AuditTrail.objects.select_related("user")[:10],
        })
        return ctx


@login_required
def stock_report(request):
    qs = (
        RouterUnit.objects.filter(is_active=True)
        .values("model__model_name", "current_stage__stage_name")
        .annotate(count=Count("id"))
        .order_by("current_stage__sequence_no", "model__model_name")
    )
    if request.GET.get("export") == "excel":
        return _export_stock_to_excel(qs)
    return render(request, "reports/stock.html", {"data": qs})


def _export_stock_to_excel(qs):
    import openpyxl
    from django.http import HttpResponse

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stock Report"
    ws.append(["Model", "Stage", "Count"])
    for row in qs:
        ws.append([
            row["model__model_name"],
            row["current_stage__stage_name"],
            row["count"],
        ])
    resp = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    resp["Content-Disposition"] = "attachment; filename=stock_report.xlsx"
    wb.save(resp)
    return resp
