from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MealPlan, Day, Meal
from .forms import MealPlanForm, MealSelectionForm
from recipes.models import Recipe
from datetime import timedelta
from django.db import transaction
from . import forms
from django.contrib import messages


@login_required
def create_meal_plan(request):
    if request.method == 'POST':
        form = MealPlanForm(request.POST)
        if form.is_valid():
            meal_plan = form.save(commit=False)
            meal_plan.user = request.user
            meal_plan.save()
            
            # Create days for the meal plan
            current_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            while current_date <= end_date:
                Day.objects.create(meal_plan=meal_plan, date=current_date)
                current_date += timedelta(days=1)
            
            return redirect('meal_plans:select_meals', meal_plan_id=meal_plan.id)
    else:
        form = MealPlanForm()
    
    return render(request, 'meal_plans/create.html', {'form': form})

@login_required
def select_meals(request, meal_plan_id):
    meal_plan = MealPlan.objects.get(id=meal_plan_id, user=request.user)
    days = meal_plan.days.all()
    recipes = Recipe.objects.all()
    
    if request.method == 'POST':
        # Debug: Print all submitted data
        print("Submitted data:", request.POST)
        form = MealSelectionForm(request.POST, recipes=recipes, days=days, 
                               meal_types=Meal.MEAL_TYPES)
        if form.is_valid():
            # Clear existing meals
            with transaction.atomic():  # Ensure all operations complete
                # First clear all existing meals for this plan
                Meal.objects.filter(day__meal_plan=meal_plan).delete()
            # Meal.objects.filter(day__meal_plan=meal_plan).delete()
            
                print("Deleted all existing meals")
            
                # Process each submitted field
                for key, recipe_id in request.POST.items():
                    if key.startswith('day_') and recipe_id:  # Only process fields with values
                        try:
                            # Parse day_id and meal_type from field name
                            parts = key.split('_')
                            day_id = int(parts[1])
                            meal_type = parts[3]  # Format: day_X_meal_Y
                            
                            # Create new meal
                            Meal.objects.create(
                                day_id=day_id,
                                meal_type=meal_type,
                                recipe_id=recipe_id
                            )
                            print(f"Created meal: day {day_id} {meal_type} = {recipe_id}")
                        except (ValueError, IndexError, Recipe.DoesNotExist) as e:
                            print(f"Skipping invalid field {key}: {str(e)}")
                            continue
                      
            print("\nVerification after save:")
            verify_meals(meal_plan)
            return redirect('meal_plans:view_meal_plan', meal_plan_id=meal_plan.id)


    else:
        form = MealSelectionForm(recipes=recipes, days=days, 
                                meal_types=Meal.MEAL_TYPES)
        
    
    
    meal_selections = {}
    for day in days:
        day_meals = {m.meal_type: m.recipe_id for m in day.meals.all()}
        meal_selections[day.id] = day_meals
    meal_fields = list(form.get_meal_fields()) if hasattr(form, 'get_meal_fields') else []

    return render(request, 'meal_plans/select_meals.html', {
        'form': form,
        'meal_plan': meal_plan,
        'days': days,
        'meal_types': Meal.MEAL_TYPES,
        'recipes': recipes,
        'meal_selections': meal_selections
    })

def verify_meals(meal_plan):
    """Verify meals were properly saved"""
    from django.db import connection
    
    print("\n=== DATABASE STATE ===")
    print("All meals in database:", Meal.objects.count())
    
    # Check connection queries
    print("\nRecent queries:")
    for q in connection.queries[-2:]:  # Show last 2 queries
        print(q['sql'])
    
    # Check actual meals
    print("\nMeals for this plan:")
    days = meal_plan.days.all().prefetch_related('meals__recipe')
    for day in days:
        meals = day.meals.all()
        print(f"\nDay {day.date} ({meals.count()} meals):")
        for meal in meals:
            print(f"- {meal.meal_type}: {meal.recipe.title if meal.recipe else 'None'}")


@login_required
def view_meal_plan(request, meal_plan_id):
    meal_plan = MealPlan.objects.get(id=meal_plan_id, user=request.user)
    days = meal_plan.days.all().prefetch_related('meals__recipe')
    recipes = Recipe.objects.all()
    return render(request, 'meal_plans/view.html', {
        'meal_plan': meal_plan,
        'days': days,
        'recipes': recipes
    })

def meal_plans_list(request):
    meal_plans = MealPlan.objects.all().order_by('-created_at')
    return render(request, 'meal_plans/meal_plans_list.html', {'meal_plans': meal_plans})



@login_required
def meal_plan_delete(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)
    
    if request.method == "POST":
        meal_plan.delete()
        messages.success(request, "Meal Plan deleted successfully!")
        return redirect("meal_plans:list")
    
    return render(request, 'meal_plans/meal_plan_confirm_delete.html', {'meal_plan': meal_plan})