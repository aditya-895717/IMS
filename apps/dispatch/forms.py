from django import forms
from .models import DispatchEntry, DispatchItem


class DispatchEntryForm(forms.ModelForm):
    class Meta:
        model = DispatchEntry
        fields = ["dispatch_date", "destination", "transporter", "vehicle_no", "challan_no", "remarks"]
        widgets = {
            "dispatch_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "destination": forms.TextInput(attrs={"class": "form-control"}),
            "transporter": forms.TextInput(attrs={"class": "form-control"}),
            "vehicle_no": forms.TextInput(attrs={"class": "form-control"}),
            "challan_no": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class DispatchItemForm(forms.ModelForm):
    class Meta:
        model = DispatchItem
        fields = ["router_unit"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.inventory.models import RouterUnit
        self.fields["router_unit"].queryset = RouterUnit.objects.filter(
            current_stage__stage_code="READY", is_active=True
        ).select_related("model", "current_stage")
        self.fields["router_unit"].widget.attrs.update({"class": "form-select"})
