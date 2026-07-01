from django.contrib import admin
from .models import Services
# Register your models here.
@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la lista
    list_display = ('name', 'description')
    
    # Buscador por texto
    search_fields = ('description', 'name')
