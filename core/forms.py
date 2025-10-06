from django import forms
from .models import Income, Expense


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["date", "service", "amount", "payment_status"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "service": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter amount in Rs"}
            ),
            "payment_status": forms.Select(attrs={"class": "form-control"}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["date", "category", "description", "amount"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "category": forms.Select(attrs={"id": "category-select"}),
            "description": forms.TextInput(
                attrs={"id": "other-description", "placeholder": "Enter other category"}
            ),
        }


# core/forms.py
from django import forms


class ReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="End Date"
    )
