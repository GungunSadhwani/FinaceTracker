# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
from datetime import date


def home(request):
    return render(request, "home.html")


# --- Income views ---
# List all incomes
def income_list(request):
    income = Income.objects.all().order_by("-date")
    return render(request, "income/income_list.html", {"income": income})


# Add a new income
def income_create(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("income_list")  # after saving, redirect to list page
    else:
        form = IncomeForm()
    return render(request, "income/income_form.html", {"form": form})


def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        income.delete()
        return redirect("income_list")
    return render(request, "income/income_confirm_delete.html", {"income": income})


# --- Expense views ---
def expenses_list(request):
    expenses = Expense.objects.all().order_by("-date")
    return render(request, "expense/expenses_list.html", {"expenses": expenses})


def expense_create(request):
    today = date.today()
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("expenses_list")
    else:
        form = ExpenseForm()
    return render(request, "expense/expense_form.html", {"form": form, "today": today})


def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
        return redirect("expenses_list")
    return render(request, "expense/expense_confirm_delete.html", {"expense": expense})


# --- Dashboard ---
def dashboard(request):
    # sum up amounts safely (Sum returns None if no rows)
    total_income = Income.objects.aggregate(total=Sum("amount"))["total"] or 0
    total_expenses = Expense.objects.aggregate(total=Sum("amount"))["total"] or 0
    net_balance = total_income - total_expenses

    context = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
    }
    return render(request, "core/dashboard.html", context)


# core/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Income, Expense
from .forms import ReportForm

from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Income, Expense


def home(request):
    return render(request, "home.html")


def report_form(request):
    return render(request, "report/report_form.html")


def generate_report(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    income_list = []
    expense_list = []
    service_summary = []
    total_income = total_expense = total_revenue = 0

    if start_date and end_date:
        income_list = Income.objects.filter(date__range=[start_date, end_date])
        expense_list = Expense.objects.filter(date__range=[start_date, end_date])

        total_income = income_list.aggregate(total=Sum("amount"))["total"] or 0
        total_expense = expense_list.aggregate(total=Sum("amount"))["total"] or 0
        total_revenue = total_income - total_expense

        service_summary = income_list.values("service").annotate(count=Count("service"))

    context = {
        "income_list": income_list,
        "expense_list": expense_list,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_revenue": total_revenue,
        "service_summary": service_summary,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(request, "report/report.html", context)


from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from django.db.models import Sum, Count
from .models import Income, Expense


def export_report_pdf(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # Fetch filtered data
    income_list = Income.objects.filter(date__range=[start_date, end_date])
    expense_list = Expense.objects.filter(date__range=[start_date, end_date])
    total_income = income_list.aggregate(total=Sum("amount"))["total"] or 0
    total_expense = expense_list.aggregate(total=Sum("amount"))["total"] or 0
    total_revenue = total_income - total_expense
    service_summary = income_list.values("service").annotate(count=Count("service"))

    # Prepare HTTP response for PDF download
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="Report_{start_date}_to_{end_date}.pdf"'
    )

    # Create PDF document
    pdf = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Report title
    elements.append(Paragraph(f"<b>Clinic Finance Report</b>", styles["Title"]))
    elements.append(Paragraph(f"Period: {start_date} to {end_date}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # INCOME TABLE
    elements.append(Paragraph("<b>Income Details</b>", styles["Heading2"]))
    income_data = [["Date", "Service", "Amount"]]
    for inc in income_list:
        income_data.append([str(inc.date), inc.service, f"{inc.amount:,.2f}"])

    income_data.append(["", "Total Income", f"{total_income:,.2f}"])

    income_table = Table(income_data, colWidths=[100, 200, 100])
    income_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]
        )
    )
    elements.append(income_table)
    elements.append(Spacer(1, 20))

    # EXPENSE TABLE
    elements.append(Paragraph("Expense Details", styles["Heading2"]))
    expense_data = [["Date", "Category", "Amount"]]
    for exp in expense_list:
        expense_data.append([str(exp.date), exp.category, f"{exp.amount:,.2f}"])

    expense_data.append(["", "Total Expense", f"{total_expense:,.2f}"])

    expense_table = Table(expense_data, colWidths=[100, 200, 100])
    expense_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightcoral),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ]
        )
    )
    elements.append(expense_table)
    elements.append(Spacer(1, 20))

    # TOTAL REVENUE SECTION
    elements.append(
        Paragraph(f"Total Revenue: {total_revenue:,.2f}", styles["Heading2"])
    )
    elements.append(Spacer(1, 20))

    # SERVICE SUMMARY TABLE
    elements.append(Paragraph("Income by Service", styles["Heading2"]))
    service_data = [["Service", "Count"]]
    for s in service_summary:
        service_data.append([s["service"], s["count"]])

    service_table = Table(service_data, colWidths=[200, 100])
    service_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgreen),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    elements.append(service_table)

    # Build and return the PDF
    pdf.build(elements)
    return response
