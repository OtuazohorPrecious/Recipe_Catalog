from django.contrib import admin
from .models import Recipe, Ingredient, Tag, RecipeIngredient


# Register all models

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3
    fields = ('ingredient', 'custom_ingredient', 'quantity')
    autocomplete_fields = ['ingredient']

#admin.site.register(Recipe)
#admin.site.register(Ingredient)
#admin.site.register(Tag)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['name'] 

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'meal_type', 'created_at')
    filter_horizontal = ('tags',)  # Makes it easier to select tags
    inlines = [RecipeIngredientInline]