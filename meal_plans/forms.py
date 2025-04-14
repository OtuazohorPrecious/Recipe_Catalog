# meal_plans/forms.py
from django import forms
from .models import MealPlan
from recipes.models import Recipe
from django.utils import timezone

class MealPlanForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = MealPlan
        fields = ['start_date', 'end_date']

class MealSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        recipes = kwargs.pop('recipes',  Recipe.objects.all())
        self.days = kwargs.pop('days', [])
        self.meal_types = kwargs.pop('meal_types', [])
        super().__init__(*args, **kwargs)
        
        for day in self.days:
            for meal_type in self.meal_types:
                field_name = f'day_{day.date}_meal_{meal_type[0]}'
                self.fields[field_name] = forms.ModelChoiceField(
                    queryset=recipes,
                    required=False,
                    widget=forms.Select(attrs={
                        'class': 'form-control recipe-select',
                        'data-day-id': day.id,
                        'data-meal-type': meal_type[0]
                    }),
                    label=''
                )
    def get_meal_fields(self):
        """Generator that yields (day, meal_type, field) tuples"""
        for day in self.days:
            for meal_type in self.meal_types:
                date_str = day.date.strftime('%Y-%m-%d')
                field_name = f'day_{date_str}_meal_{meal_type[0]}'
                yield (day, meal_type, self[field_name])