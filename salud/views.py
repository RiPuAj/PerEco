import json
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import FoodForm, HealthProfileForm, SaludFilterForm, WeightForm
from .models import Food, HealthProfile, WeightRegister

TRUNC_BY_GROUP = {
    'day': TruncDay,
    'week': TruncWeek,
    'month': TruncMonth,
}


def _build_filter_form(request):
    return SaludFilterForm(request.GET or None)


def _apply_date_filters(queryset, filter_form):
    """Filtra un queryset por date_from/date_to si el formulario es válido."""
    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
    return queryset


def _group_by_value(filter_form):
    if filter_form.is_valid():
        return filter_form.cleaned_data.get('group_by') or 'week'
    return 'week'


@login_required
def dashboard(request):
    if request.GET:
        filter_form = SaludFilterForm(request.GET)
    else:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        filter_form = SaludFilterForm({
            'group_by': 'week',
            'date_from': week_start.isoformat(),
            'date_to': today.isoformat(),
        })
    group_by = _group_by_value(filter_form)
    trunc_fn = TRUNC_BY_GROUP[group_by]

    weights = _apply_date_filters(
        WeightRegister.objects.filter(user=request.user), filter_form
    ).order_by('date')
    foods = _apply_date_filters(
        Food.objects.filter(user=request.user), filter_form
    ).order_by('date')

    weight_series = (
        weights.annotate(period=trunc_fn('date'))
        .values('period')
        .annotate(avg_value=Avg('weight_value'))
        .order_by('period')
    )
    food_series = (
        foods.annotate(period=trunc_fn('date'))
        .values('period')
        .annotate(avg_value=Avg('kcal_value'))
        .order_by('period')
    )

    weight_labels = [row['period'].strftime('%d/%m/%Y') for row in weight_series if row['avg_value'] is not None]
    weight_values = [float(row['avg_value']) for row in weight_series if row['avg_value'] is not None]
    food_labels = [row['period'].strftime('%d/%m/%Y') for row in food_series if row['avg_value'] is not None]
    food_values = [round(float(row['avg_value']), 0) for row in food_series if row['avg_value'] is not None]

    weight_avg = weights.aggregate(avg=Avg('weight_value'))['avg']
    kcal_avg = foods.aggregate(avg=Avg('kcal_value'))['avg']

    has_weight_data = bool(weight_labels)
    has_food_data = bool(food_labels)

    profile = HealthProfile.objects.filter(user=request.user).first()
    tmb = profile.tmb() if profile else None
    maintenance = profile.maintenance_calories() if profile else None

    context = {
        'filter_form': filter_form,
        'weight_chart_labels': json.dumps(weight_labels),
        'weight_chart_values': json.dumps(weight_values),
        'food_chart_labels': json.dumps(food_labels),
        'food_chart_values': json.dumps(food_values),
        'has_weight_data': has_weight_data,
        'has_food_data': has_food_data,
        'weight_avg': round(weight_avg, 1) if weight_avg else None,
        'kcal_avg': round(kcal_avg, 0) if kcal_avg else None,
        'recent_foods': foods.order_by('-date')[:6],
        'profile': profile,
        'tmb': round(tmb, 0) if tmb else None,
        'maintenance': maintenance,
    }
    return render(request, 'salud/dashboard.html', context)


@login_required
def profile_edit(request):
    profile = HealthProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = HealthProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil guardado correctamente.')
            return redirect('salud:dashboard')
    else:
        form = HealthProfileForm(instance=profile, user=request.user)
    return render(request, 'salud/profile_form.html', {'form': form, 'object': profile})


# --- Peso -------------------------------------------------------------

@login_required
def weight_list(request):
    filter_form = _build_filter_form(request)
    weights = _apply_date_filters(
        WeightRegister.objects.filter(user=request.user), filter_form
    )
    paginator = Paginator(weights, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'salud/weight_list.html', {
        'weights': page_obj,
        'filter_form': filter_form,
    })


@login_required
def weight_create(request):
    if request.method == 'POST':
        form = WeightForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Peso registrado correctamente.')
            return redirect('salud:weight_list')
    else:
        form = WeightForm(user=request.user)
    return render(request, 'salud/weight_form.html', {'form': form})


@login_required
def weight_update(request, pk):
    weight = get_object_or_404(WeightRegister, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WeightForm(request.POST, instance=weight, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro actualizado.')
            return redirect('salud:weight_list')
    else:
        form = WeightForm(instance=weight, user=request.user)
    return render(request, 'salud/weight_form.html', {'form': form, 'object': weight})


@login_required
def weight_delete(request, pk):
    weight = get_object_or_404(WeightRegister, pk=pk, user=request.user)
    if request.method == 'POST':
        weight.delete()
        messages.success(request, 'Registro eliminado.')
        return redirect('salud:weight_list')
    return render(request, 'salud/confirm_delete.html', {
        'object': weight,
        'cancel_url': reverse('salud:weight_list'),
    })


# --- Comidas ------------------------------------------------------------

@login_required
def food_list(request):
    filter_form = _build_filter_form(request)
    foods = _apply_date_filters(
        Food.objects.filter(user=request.user), filter_form
    )
    paginator = Paginator(foods, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'salud/food_list.html', {
        'foods': page_obj,
        'filter_form': filter_form,
    })


@login_required
def food_create(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comida registrada correctamente.')
            return redirect('salud:food_list')
    else:
        form = FoodForm(user=request.user)
    return render(request, 'salud/food_form.html', {'form': form})


@login_required
def food_update(request, pk):
    food = get_object_or_404(Food, pk=pk, user=request.user)
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comida actualizada.')
            return redirect('salud:food_list')
    else:
        form = FoodForm(instance=food, user=request.user)
    return render(request, 'salud/food_form.html', {'form': form, 'object': food})


@login_required
def food_delete(request, pk):
    food = get_object_or_404(Food, pk=pk, user=request.user)
    if request.method == 'POST':
        food.delete()
        messages.success(request, 'Comida eliminada.')
        return redirect('salud:food_list')
    return render(request, 'salud/confirm_delete.html', {
        'object': food,
        'cancel_url': reverse('salud:food_list'),
    })
