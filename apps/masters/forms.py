from django import forms
from .models import RouterModel, SparePart, LocationMaster


class RouterModelForm(forms.ModelForm):
    class Meta:
        model = RouterModel
        fields = ["model_name", "airtel_model_code", "category", "brand", "specifications", "is_active"]
        widgets = {
            "model_name": forms.TextInput(attrs={"class": "form-control"}),
            "airtel_model_code": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "brand": forms.TextInput(attrs={"class": "form-control"}),
            "specifications": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ["part_code", "part_name", "current_stock", "min_stock", "unit", "location"]
        widgets = {
            "part_code": forms.TextInput(attrs={"class": "form-control"}),
            "part_name": forms.TextInput(attrs={"class": "form-control"}),
            "current_stock": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "min_stock": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "unit": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.Select(attrs={"class": "form-select"}),
        }


class LocationMasterForm(forms.ModelForm):
    class Meta:
        model = LocationMaster
        fields = ["location_code", "location_name", "description"]
        widgets = {
            "location_code": forms.TextInput(attrs={"class": "form-control"}),
            "location_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
