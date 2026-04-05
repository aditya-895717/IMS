from django import forms
from .models import InwardEntry, InwardItem


class InwardEntryForm(forms.ModelForm):
    class Meta:
        model = InwardEntry
        fields = ["inward_date", "source_name", "vehicle_no", "challan_no", "remarks", "document"]
        widgets = {
            "inward_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "source_name": forms.TextInput(attrs={"class": "form-control"}),
            "vehicle_no": forms.TextInput(attrs={"class": "form-control"}),
            "challan_no": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "document": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class InwardItemForm(forms.ModelForm):
    class Meta:
        model = InwardItem
        exclude = ["inward_entry"]
        widgets = {
            "serial_number": forms.TextInput(attrs={"class": "form-control"}),
            "mac_address": forms.TextInput(attrs={"class": "form-control"}),
            "model": forms.Select(attrs={"class": "form-select"}),
            "initial_condition": forms.Select(attrs={"class": "form-select"}),
            "batch_no": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_serial_number(self):
        from apps.inventory.models import RouterUnit
        sn = self.cleaned_data["serial_number"].strip().upper()
        if RouterUnit.objects.filter(serial_number=sn).exists():
            raise forms.ValidationError(f"Serial '{sn}' already registered.")
        return sn

    def clean_mac_address(self):
        from apps.inventory.models import RouterUnit
        mac = self.cleaned_data["mac_address"].strip().upper()
        if RouterUnit.objects.filter(mac_address=mac).exists():
            raise forms.ValidationError(f"MAC '{mac}' already registered.")
        return mac


InwardItemFormSet = forms.formset_factory(
    InwardItemForm, extra=1, can_delete=True, min_num=1, validate_min=True
)
