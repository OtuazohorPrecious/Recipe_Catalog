from django.contrib import admin
from .models import Recipe, Tag


# Register all models



#admin.site.register(Recipe)
#admin.site.register(Ingredient)
#admin.site.register(Tag)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'meal_type', 'created_at')
    filter_horizontal = ('tags',)  # Makes it easier to select tags