from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    # Income
    path("income/", views.income_list, name="income_list"),
    path("income/add/", views.income_create, name="income_create"),
    path("income/<int:pk>/delete/", views.income_delete, name="income_delete"),
    # Expense
    path("expenses/", views.expenses_list, name="expenses_list"),
    path("expenses/add/", views.expense_create, name="expense_create"),
    # path("expenses/<int:pk>/edit/", views.expense_edit, name="expense_edit"),  # Optional
    path("expenses/<int:pk>/delete/", views.expense_delete, name="expense_delete"),
    path("report/form/", views.report_form, name="report_form"),  # Form page
    path(
        "report/result/", views.generate_report, name="generate_report"
    ),  # Report result
    path("report/pdf/", views.export_report_pdf, name="export_report_pdf"),
]
