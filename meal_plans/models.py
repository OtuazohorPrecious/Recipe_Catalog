

# Create your models here.
from django.db import models
from recipes.models import Recipe
from django.contrib.auth import get_user_model

User = get_user_model()

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Day(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='days')
    date = models.DateField()
    def get_total_calories(self):
        total = 0
        for meal in self.meals.all():
            if meal.recipe and meal.recipe.estimated_calories:
                total += meal.recipe.estimated_calories
        return total if total > 0 else None

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('desert', 'Desert'),
        ('snack', 'Snack'),
    ]
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='meals')
    notes = models.TextField(blank=True)
    class Meta:
        unique_together = ('day', 'meal_type')