from django.contrib import admin

from .models import Category, Expense, FutureExpense, Income, Investment

admin.site.register(Category)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Investment)
admin.site.register(FutureExpense)
