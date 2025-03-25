from django.db import models
from django.contrib.auth.models import User




class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

 

class Recipe(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('desert', 'Desert'),
        ('snack', 'Snack'),
    ]
    #TAG_CHOICES  #learn more here https://www.northshore.org/healthy-you/vegan-flexitarian-vegetarian-pescatarian-and-macrobiotic-diets--whats-the-difference/

    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField()
    instructions = models.TextField()
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPE_CHOICES, null=True)
    banner = models.ImageField(default= 'fallback.png', blank = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='recipes')
    ingredients = models.ManyToManyField(
        Ingredient, 
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        blank=True
    )



    def __str__(self):
        return self.title
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True, blank=True)
    custom_ingredient = models.CharField(max_length=100, blank=True)  # For manual entry
    quantity = models.CharField(max_length=50, blank = True)
    
    def get_ingredient_name(self):
        return self.ingredient.name if self.ingredient else self.custom_ingredient
    
    def __str__(self):
        return f"{self.quantity} {self.ingredient.name}"
