from django import forms
from core.forms import BRLDecimalField
from .models import Ministry, MinistryBudget

class MinistryForm(forms.ModelForm):
    class Meta:
        model = Ministry
        fields = ("name", "description", "active")
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items(): field.widget.attrs.setdefault("class", "form-check-input" if name == "active" else "form-control")

class MinistryBudgetForm(forms.ModelForm):
    amount = BRLDecimalField(label="Orçamento", min_value=0, widget=forms.TextInput(attrs={"class": "form-control", "data-currency": "brl", "inputmode": "decimal"}))
    class Meta:
        model = MinistryBudget
        fields = ("ministry", "year", "month", "amount", "notes")
        widgets = {"ministry": forms.Select(attrs={"class": "form-select"}), "year": forms.NumberInput(attrs={"class": "form-control", "min": 2024}), "month": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 12}), "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ministry"].label = "Departamento"
