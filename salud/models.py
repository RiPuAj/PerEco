from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User


class HealthProfile(models.Model):
    SEX_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    ACTIVITY_CHOICES = [
        (Decimal('1.200'), 'Sedentario (poco o ningún ejercicio)'),
        (Decimal('1.375'), 'Ligero (1-3 días/semana)'),
        (Decimal('1.550'), 'Moderado (3-5 días/semana)'),
        (Decimal('1.725'), 'Activo (6-7 días/semana)'),
        (Decimal('1.900'), 'Muy activo (ejercicio intenso diario)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
    height = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Altura (cm)')
    birth_date = models.DateField(verbose_name='Fecha de nacimiento')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name='Sexo')
    activity_factor = models.DecimalField(max_digits=4, decimal_places=3, choices=ACTIVITY_CHOICES, verbose_name='Factor de actividad')

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def tmb(self):
        """Mifflin-St Jeor: TMB = 10*peso + 6.25*altura - 5*edad + sexo_ajuste"""
        from django.db.models import Avg
        weight_avg = WeightRegister.objects.filter(user=self.user).aggregate(avg=Avg('weight_value'))['avg']
        if weight_avg is None:
            return None
        peso = float(weight_avg)
        altura = float(self.height)
        edad = self.age()
        if self.sex == 'M':
            return 10 * peso + 6.25 * altura - 5 * edad + 5
        else:
            return 10 * peso + 6.25 * altura - 5 * edad - 161

    def maintenance_calories(self):
        tmb = self.tmb()
        if tmb is None:
            return None
        return round(tmb * float(self.activity_factor))


class WeightRegister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight_value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.date} - {self.weight_value} kg"
    

class Food(models.Model):
    MOMENTS_ENUM = [
        ('desayuno', 'Desayuno'),
        ('almuerzo', 'Almuerzo'),
        ('cena', 'Cena'),
        ('snack', 'Snack/Otros')
    ] 

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    moment_day = models.CharField(max_length=10, choices=MOMENTS_ENUM)
    kcal_value = models.IntegerField(null=True)
    description = models.TextField()


    def __str__(self) -> str:
        return f"{self.date} ({self.moment_day})"