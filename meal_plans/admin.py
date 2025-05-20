from django.contrib import admin
from .models import Meal, MealPlan
# Register your models here.


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'meal_type')

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'created_at')