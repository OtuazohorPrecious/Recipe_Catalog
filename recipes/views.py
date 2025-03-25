from django.shortcuts import render, redirect
from .models import Recipe, Tag
from django.contrib.auth.decorators import login_required
from . import forms
from django.db.models import Q


# Create your views here.
def recipes_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipes_list.html', {'recipes': recipes})

def recipe_page(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    return render(request, 'recipes/recipe_page.html', {'recipe': recipe})

@login_required(login_url="users/login/")
def recipe_new(request):
    if request.method == "POST":
        form = forms.createRecipe(request.POST, request.FILES)
        if form.is_valid():
            #save with user
            newrecipe=form.save(commit=False)
            newrecipe.created_by=request.user
            newrecipe.save()
            return redirect("recipes:list")
    else:
        form = forms.createRecipe()
    return render(request, 'recipes/recipe_new.html', {'form': form})



def recipe_search(request):
    query = request.GET.get('q', '')
    meal_type = request.GET.get('meal_type', '')
    tag_ids = request.GET.getlist('tags')  # For multiple tag selection
    
    recipes = Recipe.objects.all()
    
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) |
            Q(recipeingredient__ingredient__name__icontains=query)
        ).distinct()
    
    if meal_type:
        recipes = recipes.filter(meal_type=meal_type)
    
    if tag_ids:
        recipes = recipes.filter(tags__id__in=tag_ids)
    
    # Get all tags for the filter sidebar
    all_tags = Tag.objects.all()
    
    context = {
        'recipes': recipes,
        'query': query,
        'all_tags': all_tags,
        'selected_tags': tag_ids,
        'selected_meal_type': meal_type
    }
    return render(request, 'recipes/search.html', context)