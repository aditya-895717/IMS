from django import forms


class RouterSearchForm(forms.Form):
    serial = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control", "placeholder": "Search serial number...",
        }),
    )
    stage = forms.CharField(
        max_length=20, required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = forms.CharField(
        max_length=20, required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.masters.models import StageMaster
        stage_choices = [("", "All Stages")] + list(
            StageMaster.objects.values_list("stage_code", "stage_name")
        )
        status_choices = [("", "All Statuses"), ("active", "Active"), ("hold", "On Hold"),
                          ("scrap", "Scrapped"), ("dispatched", "Dispatched")]
        self.fields["stage"].widget.choices = stage_choices
        self.fields["status"].widget.choices = status_choices
