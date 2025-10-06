from django.db import models

# core/models.py
from django.db import models


class Income(models.Model):
    SERVICE_CHOICES = [
        ("OPD", "OPD"),
        ("Labs", "Labs"),
        ("CT", "CT"),
        ("MRI", "MRI"),
        ("Endoscopy", "Endoscopy"),
        ("EU Diagnostics", "EU Diagnostics"),
        ("ERCP", "ERCP"),
        ("EUS Interventional", "EUS Interventional"),
        ("ANCILLARY SERVICES", "ANCILLARY SERVICES"),
    ]

    date = models.DateField()
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[("Paid", "Paid"), ("Pending", "Pending")],
        default="Paid",
    )

    def __str__(self):
        return f"{self.service} - {self.amount} Rs on {self.date}"


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("Salary", "Salary"),
        ("Bills", "Bills"),
        ("Rent", "Rent"),
        ("Transport", "Transport"),
        ("Other", "Other"),
    ]

    date = models.DateField()
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="other"
    )
    description = models.CharField(
        max_length=255, blank=True, null=True
    )  # used only if category=Other
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.category == "Other" and self.description:
            return (
                f"{self.date} - {self.category} ({self.description}) - Rs {self.amount}"
            )
        return f"{self.date} - {self.category} - Rs {self.amount}"
