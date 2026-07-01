import json
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import (CategoryForm, ExpenseForm, FutureExpenseForm,
                    IncomeForm, InvestmentForm)
from .models import Category, Expense, FutureExpense, Income, Investment


# --- Helpers ---------------------------------------------------------------

def _paginate(request, queryset, per_page=20):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get('page'))


# --- Dashboard -------------------------------------------------------------

@login_required
def dashboard(request):
    today = date.today()
    month_start = today.replace(day=1)

    # Ingresos del mes
    incomes_month = Income.objects.filter(user=request.user, date__gte=month_start, date__lte=today)
    total_income_month = incomes_month.aggregate(s=Sum('amount'))['s'] or 0

    # Gastos del mes
    expenses_month = Expense.objects.filter(user=request.user, date__gte=month_start, date__lte=today)
    total_expense_month = expenses_month.aggregate(s=Sum('amount'))['s'] or 0

    # Balance
    balance_month = float(total_income_month) - float(total_expense_month)

    # Totales generales
    total_incomes = Income.objects.filter(user=request.user).aggregate(s=Sum('amount'))['s'] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(s=Sum('amount'))['s'] or 0

    # Gastos totales futuros
    total_future = FutureExpense.objects.filter(user=request.user).aggregate(s=Sum('estimated_amount'))['s'] or 0

    # Inversiones
    investments = Investment.objects.filter(user=request.user)
    total_invested = investments.aggregate(s=Sum('amount_invested'))['s'] or 0
    total_current = investments.aggregate(s=Sum('current_value'))['s'] or 0

    # Gastos por categoría (últimos 12 meses)
    twelve_months_ago = today - timedelta(days=365)
    expenses_by_category = (
        Expense.objects.filter(user=request.user, date__gte=twelve_months_ago)
        .values('category__name', 'category__color')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    expense_cat_labels = [e['category__name'] or 'Sin categoría' for e in expenses_by_category]
    expense_cat_values = [float(e['total']) for e in expenses_by_category]
    expense_cat_colors = [e['category__color'] or '#94a3b8' for e in expenses_by_category]

    # Gastos máximo permitido (ingresos - ahorro)
    max_expenses = float(total_income_month) if total_income_month else 0
    savings_target = float(total_income_month) * 0.2 if total_income_month else 0

    context = {
        'total_income_month': float(total_income_month),
        'total_expense_month': float(total_expense_month),
        'balance_month': balance_month,
        'balance_class': 'text-green-600' if balance_month >= 0 else 'text-red-600',
        'total_incomes': float(total_incomes),
        'total_expenses': float(total_expenses),
        'total_future': float(total_future),
        'total_invested': float(total_invested),
        'total_current': float(total_current),
        'investments_count': investments.count(),
        'max_expenses': max_expenses,
        'savings_target': savings_target,
        'max_spendable': max_expenses - savings_target,
        'expense_cat_labels': json.dumps(expense_cat_labels),
        'expense_cat_values': json.dumps(expense_cat_values),
        'expense_cat_colors': json.dumps(expense_cat_colors),
        'has_expense_cat_data': bool(expense_cat_labels),
        'recent_expenses': Expense.objects.filter(user=request.user).order_by('-date')[:5],
        'recent_incomes': Income.objects.filter(user=request.user).order_by('-date')[:5],
    }
    return render(request, 'finanzas/dashboard.html', context)


# --- Ingresos --------------------------------------------------------------

@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'finanzas/income_list.html', {'incomes': _paginate(request, incomes)})


@login_required
def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingreso registrado correctamente.')
            return redirect('finanzas:income_list')
    else:
        form = IncomeForm(user=request.user)
    return render(request, 'finanzas/income_form.html', {'form': form})


@login_required
def income_update(request, pk):
    obj = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingreso actualizado.')
            return redirect('finanzas:income_list')
    else:
        form = IncomeForm(instance=obj, user=request.user)
    return render(request, 'finanzas/income_form.html', {'form': form, 'object': obj})


@login_required
def income_delete(request, pk):
    obj = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Ingreso eliminado.')
        return redirect('finanzas:income_list')
    return render(request, 'finanzas/confirm_delete.html', {
        'object': obj,
        'cancel_url': reverse('finanzas:income_list'),
    })


# --- Gastos ----------------------------------------------------------------

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'finanzas/expense_list.html', {'expenses': _paginate(request, expenses)})


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto registrado correctamente.')
            return redirect('finanzas:expense_list')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'finanzas/expense_form.html', {'form': form})


@login_required
def expense_update(request, pk):
    obj = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto actualizado.')
            return redirect('finanzas:expense_list')
    else:
        form = ExpenseForm(instance=obj, user=request.user)
    return render(request, 'finanzas/expense_form.html', {'form': form, 'object': obj})


@login_required
def expense_delete(request, pk):
    obj = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Gasto eliminado.')
        return redirect('finanzas:expense_list')
    return render(request, 'finanzas/confirm_delete.html', {
        'object': obj,
        'cancel_url': reverse('finanzas:expense_list'),
    })


# --- Inversiones -----------------------------------------------------------

@login_required
def investment_list(request):
    investments = Investment.objects.filter(user=request.user).order_by('-purchase_date')
    total_invested = investments.aggregate(s=Sum('amount_invested'))['s'] or 0
    total_current = investments.aggregate(s=Sum('current_value'))['s'] or 0
    return render(request, 'finanzas/investment_list.html', {
        'investments': _paginate(request, investments),
        'total_invested': total_invested,
        'total_current': total_current,
    })


@login_required
def investment_create(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inversión registrada correctamente.')
            return redirect('finanzas:investment_list')
    else:
        form = InvestmentForm(user=request.user)
    return render(request, 'finanzas/investment_form.html', {'form': form})


@login_required
def investment_update(request, pk):
    obj = get_object_or_404(Investment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = InvestmentForm(request.POST, instance=obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inversión actualizada.')
            return redirect('finanzas:investment_list')
    else:
        form = InvestmentForm(instance=obj, user=request.user)
    return render(request, 'finanzas/investment_form.html', {'form': form, 'object': obj})


@login_required
def investment_delete(request, pk):
    obj = get_object_or_404(Investment, pk=pk, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Inversión eliminada.')
        return redirect('finanzas:investment_list')
    return render(request, 'finanzas/confirm_delete.html', {
        'object': obj,
        'cancel_url': reverse('finanzas:investment_list'),
    })


# --- Gastos Futuros --------------------------------------------------------

@login_required
def future_list(request):
    expenses = FutureExpense.objects.filter(user=request.user).order_by('due_date', 'priority')
    total = expenses.aggregate(s=Sum('estimated_amount'))['s'] or 0
    return render(request, 'finanzas/future_list.html', {
        'future_expenses': _paginate(request, expenses),
        'total_future': total,
    })


@login_required
def future_create(request):
    if request.method == 'POST':
        form = FutureExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto futuro registrado.')
            return redirect('finanzas:future_list')
    else:
        form = FutureExpenseForm(user=request.user)
    return render(request, 'finanzas/future_form.html', {'form': form})


@login_required
def future_update(request, pk):
    obj = get_object_or_404(FutureExpense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = FutureExpenseForm(request.POST, instance=obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto futuro actualizado.')
            return redirect('finanzas:future_list')
    else:
        form = FutureExpenseForm(instance=obj, user=request.user)
    return render(request, 'finanzas/future_form.html', {'form': form, 'object': obj})


@login_required
def future_delete(request, pk):
    obj = get_object_or_404(FutureExpense, pk=pk, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Gasto futuro eliminado.')
        return redirect('finanzas:future_list')
    return render(request, 'finanzas/confirm_delete.html', {
        'object': obj,
        'cancel_url': reverse('finanzas:future_list'),
    })


# --- Categorías ------------------------------------------------------------

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user).order_by('type', 'name')
    return render(request, 'finanzas/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada.')
            return redirect('finanzas:category_list')
    else:
        form = CategoryForm(user=request.user)
    return render(request, 'finanzas/category_form.html', {'form': form})


@login_required
def category_delete(request, pk):
    obj = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Categoría eliminada.')
        return redirect('finanzas:category_list')
    return render(request, 'finanzas/confirm_delete.html', {
        'object': obj,
        'cancel_url': reverse('finanzas:category_list'),
    })
