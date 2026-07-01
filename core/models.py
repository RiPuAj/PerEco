from django.db import models

# Create your models here.

class Services(models.Model):
    name = models.CharField(max_length=100, default='No name', verbose_name="Nombre del Servicio")
    description = models.TextField(verbose_name="Descripción")
    url_name = models.CharField(max_length=100, null=True, verbose_name="Nombre de la URL (name)")
    active = models.BooleanField(default=False, verbose_name="¿Está Activo?")
    color = models.CharField(max_length=7, default="#007bff", verbose_name="Color Hexadecimal (Ej: #28a745)")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Clase del Icono (Opcional)")
    
    def __str__(self) -> str:
        return f"Service name: {self.name} with description: {self.description}"