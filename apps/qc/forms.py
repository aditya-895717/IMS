from django import forms
from .models import QCRecord


class QCRecordForm(forms.ModelForm):
    class Meta:
        model = QCRecord
        exclude = ["router_unit", "inspected_by", "inspected_at"]
        widgets = {
            "body_condition": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "serial_verified": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "mac_verified": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "performance_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "ports_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "label_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "qc_result": forms.Select(attrs={"class": "form-select"}),
            "rejection_reason": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean(self):
        data = super().clean()
        result = data.get("qc_result")
        if result == "fail" and not data.get("rejection_reason"):
            raise forms.ValidationError("Rejection reason is required when QC fails.")
        return data
