from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Ingreso'),
        ('expense', 'Gasto'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='finance_categories')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    color = models.CharField(max_length=7, default='#6366f1')

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ['user', 'name', 'type']

    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'type': 'income'})

    def __str__(self):
        return f"{self.date} - {self.amount}€"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'type': 'expense'})

    def __str__(self):
        return f"{self.date} - {self.amount}€"


class Investment(models.Model):
    TYPE_CHOICES = [
        ('stock', 'Acciones'),
        ('etf', 'ETF'),
        ('crypto', 'Criptomoneda'),
        ('real_estate', 'Inmueble'),
        ('other', 'Otro'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    name = models.CharField(max_length=200)
    investment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def profit(self):
        if self.current_value is None:
            return None
        return float(self.current_value) - float(self.amount_invested)

    def profit_percentage(self):
        if self.current_value is None or float(self.amount_invested) == 0:
            return None
        return (float(self.current_value) - float(self.amount_invested)) / float(self.amount_invested) * 100


class FutureExpense(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='future_expenses')
    name = models.CharField(max_length=200)
    estimated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'type': 'expense'})
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
