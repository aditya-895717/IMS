from django import forms
from .models import PackingRecord


class PackingRecordForm(forms.ModelForm):
    class Meta:
        model = PackingRecord
        exclude = ["router_unit", "packed_by", "packed_at"]
        widgets = {
            "box_no": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.TextInput(attrs={"class": "form-control"}),
        }
