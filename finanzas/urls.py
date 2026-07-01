from django.urls import path

from . import views

app_name = 'finanzas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Ingresos
    path('ingresos/', views.income_list, name='income_list'),
    path('ingresos/nuevo/', views.income_create, name='income_create'),
    path('ingresos/<int:pk>/editar/', views.income_update, name='income_update'),
    path('ingresos/<int:pk>/eliminar/', views.income_delete, name='income_delete'),

    # Gastos
    path('gastos/', views.expense_list, name='expense_list'),
    path('gastos/nuevo/', views.expense_create, name='expense_create'),
    path('gastos/<int:pk>/editar/', views.expense_update, name='expense_update'),
    path('gastos/<int:pk>/eliminar/', views.expense_delete, name='expense_delete'),

    # Inversiones
    path('inversiones/', views.investment_list, name='investment_list'),
    path('inversiones/nueva/', views.investment_create, name='investment_create'),
    path('inversiones/<int:pk>/editar/', views.investment_update, name='investment_update'),
    path('inversiones/<int:pk>/eliminar/', views.investment_delete, name='investment_delete'),

    # Gastos Futuros
    path('gastos-futuros/', views.future_list, name='future_list'),
    path('gastos-futuros/nuevo/', views.future_create, name='future_create'),
    path('gastos-futuros/<int:pk>/editar/', views.future_update, name='future_update'),
    path('gastos-futuros/<int:pk>/eliminar/', views.future_delete, name='future_delete'),

    # Categorías
    path('categorias/', views.category_list, name='category_list'),
    path('categorias/nueva/', views.category_create, name='category_create'),
    path('categorias/<int:pk>/eliminar/', views.category_delete, name='category_delete'),
]
