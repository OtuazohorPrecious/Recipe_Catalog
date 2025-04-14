from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Tag, Ingredient
from django.contrib.auth.decorators import login_required
from . import forms
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import RecipeRating, RecipeComment
from .forms import RatingForm, CommentForm

def is_chef(user):
    return user.user_type == 'chef'

# Create your views here.
def recipes_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes/recipes_list.html', {'recipes': recipes})

def recipe_page(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    rating_form = RatingForm()
    comment_form = CommentForm()
    
    # Check if user has already rated
    if request.user.is_authenticated:
        try:
            user_rating = RecipeRating.objects.get(recipe=recipe, user=request.user)
            rating_form = RatingForm(initial={'rating': user_rating.rating})
        except RecipeRating.DoesNotExist:
            pass
    
    context = {
        'recipe': recipe,
        'rating_form': rating_form,
        'comment_form': comment_form,
    }
    return render(request, 'recipes/recipe_page.html', context)

@require_http_methods(["GET"])
def ingredient_search(request):
    """Basic search endpoint"""
    search_term = request.GET.get('search', '')
    ingredients = Ingredient.objects.filter(name__icontains=search_term)[:5]
    results = [{'name': i.name, 'id': i.id} for i in ingredients]
    return JsonResponse(results, safe=False)

def add_ingredient(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()  # Use request.POST, not request.FILES
        
        if name:  # Only create if name is not empty
            # get_or_create returns a tuple: (object, created)
            ingredient, created = Ingredient.objects.get_or_create(name=name)
            
            # No need for .add() here - get_or_create already saves to database
            return redirect('recipes:new-recipe')  # Redirect to a list view
            
    return render(request, 'recipes/add_ingredient.html')

@user_passes_test(is_chef)
def recipe_new(request):
    if request.method == "POST":
        form = forms.createRecipe(request.POST, request.FILES)
        if form.is_valid():
            #save with user
            newrecipe=form.save(commit=False)
            newrecipe.created_by=request.user
            newrecipe.save()

            for ingredient in form.cleaned_data['ingredients']:
                newrecipe.ingredients.add(ingredient)
            for tag in form.cleaned_data['tags']:
                newrecipe.tags.add(tag)
        
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




@login_required
def recipe_edit(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, created_by=request.user)
    
    if request.method == "POST":
        form = forms.createRecipe(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            edited_recipe = form.save()
            
            # Clear existing many-to-many relationships
            edited_recipe.ingredients.clear()
            edited_recipe.tags.clear()
            
            # Add new relationships
            for ingredient in form.cleaned_data['ingredients']:
                edited_recipe.ingredients.add(ingredient)
            for tag in form.cleaned_data['tags']:
                edited_recipe.tags.add(tag)
            
            messages.success(request, "Recipe updated successfully!")
            return redirect("recipes:page", slug=edited_recipe.slug)
    else:
        form = forms.createRecipe(instance=recipe)
        # Set initial values for many-to-many fields
        form.fields['ingredients'].initial = recipe.ingredients.all()
        form.fields['tags'].initial = recipe.tags.all()
    
    return render(request, 'recipes/recipe_edit.html', {'form': form, 'recipe': recipe})

@login_required
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, created_by=request.user)
    
    if request.method == "POST":
        recipe.delete()
        messages.success(request, "Recipe deleted successfully!")
        return redirect("recipes:list")
    
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


def rate_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = RecipeRating.objects.update_or_create(
                recipe=recipe,
                user=request.user,
                defaults={'rating': form.cleaned_data['rating']}
            )
            messages.success(request, 'Your rating has been saved!')
    return redirect('recipes:page', slug=slug)

def add_comment(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            RecipeComment.objects.create(
                recipe=recipe,
                user=request.user,
                text=form.cleaned_data['text']
            )
            messages.success(request, 'Your comment has been posted!')
    return redirect('recipes:page', slug=slug)

def delete_comment(request, comment_id):
    comment = get_object_or_404(RecipeComment, id=comment_id, user=request.user)
    recipe_slug = comment.recipe.slug
    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect('recipes:page', slug=recipe_slug)