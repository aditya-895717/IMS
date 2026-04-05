from django import forms
from .models import RepairRecord, RepairPartUsage


class RepairRecordForm(forms.ModelForm):
    class Meta:
        model = RepairRecord
        exclude = ["router_unit", "repaired_by"]
        widgets = {
            "repair_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "issue_type": forms.TextInput(attrs={"class": "form-control"}),
            "diagnosis": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "action_taken": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "repair_status": forms.Select(attrs={"class": "form-select"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class RepairPartUsageForm(forms.ModelForm):
    class Meta:
        model = RepairPartUsage
        fields = ["spare_part", "qty_used"]
        widgets = {
            "spare_part": forms.Select(attrs={"class": "form-select"}),
            "qty_used": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


RepairPartFormSet = forms.inlineformset_factory(
    RepairRecord, RepairPartUsage,
    form=RepairPartUsageForm,
    extra=1, can_delete=True,
)
