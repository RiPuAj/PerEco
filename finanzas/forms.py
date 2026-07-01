from django import forms

from .models import Category, Expense, FutureExpense, Income, Investment

INPUT_CLASSES = (
    'block w-full rounded-lg border-stone-300 dark:border-stone-600 '
    'dark:bg-stone-700 dark:text-stone-200 text-sm shadow-sm '
    'focus:border-blue-500 focus:ring-blue-500'
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ej: Nómina'}),
            'type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'h-10 w-full rounded-lg border-stone-300 cursor-pointer'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self._user is not None:
            instance.user = self._user
        if commit:
            instance.save()
        return instance


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'amount', 'description', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': INPUT_CLASSES, 'placeholder': '1500.00'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': INPUT_CLASSES, 'placeholder': 'Descripción opcional'}),
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user, type='income')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self._user is not None:
            instance.user = self._user
        if commit:
            instance.save()
        return instance


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'amount', 'description', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': INPUT_CLASSES, 'placeholder': '45.50'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': INPUT_CLASSES, 'placeholder': 'Descripción opcional'}),
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user, type='expense')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self._user is not None:
            instance.user = self._user
        if commit:
            instance.save()
        return instance


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['name', 'investment_type', 'amount_invested', 'current_value', 'purchase_date', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ej: S&P 500 ETF'}),
            'investment_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'amount_invested': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': INPUT_CLASSES, 'placeholder': '10000.00'}),
            'current_value': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': INPUT_CLASSES, 'placeholder': '12000.00'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': INPUT_CLASSES, 'placeholder': 'Notas opcionales'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self._user is not None:
            instance.user = self._user
        if commit:
            instance.save()
        return instance


class FutureExpenseForm(forms.ModelForm):
    class Meta:
        model = FutureExpense
        fields = ['name', 'estimated_amount', 'due_date', 'category', 'priority', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Ej: Cambio de coche'}),
            'estimated_amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': INPUT_CLASSES, 'placeholder': '15000.00'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'priority': forms.Select(attrs={'class': INPUT_CLASSES}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': INPUT_CLASSES, 'placeholder': 'Notas opcionales'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user, type='expense')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self._user is not None:
            instance.user = self._user
        if commit:
            instance.save()
        return instance
