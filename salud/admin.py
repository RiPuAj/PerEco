from django.contrib import admin
from .models import Food, HealthProfile, WeightRegister

# Register your models here.
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la lista
    list_display = ('date', 'moment_day', 'kcal_value', 'user')
    
    # Filtros laterales para buscar rápido
    list_filter = ('date', 'moment_day', 'user')
    
    # Buscador por texto
    search_fields = ('description', 'user__username')


admin.site.register(WeightRegister)
admin.site.register(HealthProfile)