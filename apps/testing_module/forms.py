from django import forms
from .models import TestRecord


class TestRecordForm(forms.ModelForm):
    class Meta:
        model = TestRecord
        exclude = ["router_unit", "tested_by", "tested_at", "is_retest"]
        widgets = {
            "power_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "boot_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "wifi_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "lan_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "led_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "adapter_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "firmware_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "reset_button_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "overall_result": forms.Select(attrs={"class": "form-select"}),
            "fail_reason": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean(self):
        data = super().clean()
        checks = [
            "power_ok", "boot_ok", "wifi_ok", "lan_ok",
            "led_ok", "adapter_ok", "firmware_ok", "reset_button_ok",
        ]
        failed = [c for c in checks if not data.get(c)]
        result = data.get("overall_result")
        if failed and result == "pass":
            raise forms.ValidationError("Cannot mark Pass when checks are failing.")
        if not failed and result == "fail":
            raise forms.ValidationError("Cannot mark Fail when all checks pass.")
        if result == "fail" and not data.get("fail_reason"):
            raise forms.ValidationError("Fail reason is required when result is Fail.")
        return data
