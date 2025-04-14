from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from recipes.models import Recipe

def homepage(request):
    #return HttpResponse("Hello World!")
    # Get 3 featured recipes for carousel
    featured_recipes = Recipe.objects.filter(is_featured=True)[:3]
    
    # Get 3 more recipes for the grid
    other_recipes = Recipe.objects.exclude(
        id__in=[r.id for r in featured_recipes]
    )[:3]
    print("Featured Recipes:", list(featured_recipes))
    print("other Recipes:", list(other_recipes))
    context = {
        'featured_recipes': featured_recipes,
        'other_recipes': other_recipes,
    }
    return render(request, 'home.html', context)

def about(request):
    #return HttpResponse("My about page")
    return render(request, 'about.html')