from django import forms

from .models import Food, HealthProfile, WeightRegister

INPUT_CLASSES = (
    'block w-full rounded-lg border-stone-300 dark:border-stone-600 dark:bg-stone-700 dark:text-stone-200 '
    'text-sm shadow-sm focus:border-brand-500 focus:ring-brand-500'
)


class WeightForm(forms.ModelForm):
    class Meta:
        model = WeightRegister
        fields = ['date', 'weight_value']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'weight_value': forms.NumberInput(attrs={
                'step': '0.1', 'min': '0', 'class': INPUT_CLASSES, 'placeholder': '70.5',
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        if date and self._user is not None:
            qs = WeightRegister.objects.filter(user=self._user, date=date)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('date', 'Ya existe un registro de peso para esta fecha.')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self._user is not None:
            instance.user = self._user
        if commit:
            instance.save()
        return instance


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['date', 'moment_day', 'kcal_value', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'moment_day': forms.Select(attrs={'class': INPUT_CLASSES}),
            'kcal_value': forms.NumberInput(attrs={'min': '0', 'class': INPUT_CLASSES, 'placeholder': '550'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': INPUT_CLASSES, 'placeholder': 'Ej: pollo a la plancha con arroz'}),
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


class SaludFilterForm(forms.Form):
    GROUP_BY_CHOICES = [
        ('day', 'Día'),
        ('week', 'Semana'),
        ('month', 'Mes'),
    ]

    group_by = forms.ChoiceField(
        choices=GROUP_BY_CHOICES, required=False, initial='week',
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
    )

    @property
    def group_by_choices(self):
        return self.GROUP_BY_CHOICES

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError('La fecha "Desde" no puede ser posterior a "Hasta".')
        return cleaned_data


class HealthProfileForm(forms.ModelForm):
    class Meta:
        model = HealthProfile
        fields = ['height', 'birth_date', 'sex', 'activity_factor']
        widgets = {
            'height': forms.NumberInput(attrs={
                'step': '0.1', 'min': '0', 'class': INPUT_CLASSES, 'placeholder': '170',
            }),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'sex': forms.Select(attrs={'class': INPUT_CLASSES}),
            'activity_factor': forms.Select(attrs={'class': INPUT_CLASSES}),
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
