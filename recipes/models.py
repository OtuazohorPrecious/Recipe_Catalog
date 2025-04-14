from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator




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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='recipes')
    ingredients = models.ManyToManyField(
        Ingredient, 
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        blank=True
    )
    is_featured = models.BooleanField(default=False)
    @property
    def average_rating(self):
        from django.db.models import Avg
        return self.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    
    def get_star_rating(self):
        full_stars = int(self.average_rating)
        half_star = (self.average_rating - full_stars) >= 0.5
        empty_stars = 5 - full_stars - (1 if half_star else 0)
        return {
            'full': full_stars,
            'half': half_star,
            'empty': empty_stars
        }
    



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
    

class RecipeRating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user')  # Each user can rate a recipe only once

class RecipeComment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"