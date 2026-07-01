from django.urls import path

from . import views

app_name = 'salud'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('perfil/', views.profile_edit, name='profile_edit'),

    path('peso/', views.weight_list, name='weight_list'),
    path('peso/nuevo/', views.weight_create, name='weight_create'),
    path('peso/<int:pk>/editar/', views.weight_update, name='weight_update'),
    path('peso/<int:pk>/eliminar/', views.weight_delete, name='weight_delete'),

    path('comidas/', views.food_list, name='food_list'),
    path('comidas/nueva/', views.food_create, name='food_create'),
    path('comidas/<int:pk>/editar/', views.food_update, name='food_update'),
    path('comidas/<int:pk>/eliminar/', views.food_delete, name='food_delete'),
]
