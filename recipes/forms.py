from django import forms
from . import models

from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = models.RecipeIngredient
        fields = '__all__'
    
    def clean(self):
        if not self.cleaned_data.get('ingredient') and not self.cleaned_data.get('custom_ingredient'):
            raise ValidationError("You must either select an ingredient or enter a custom one")



class createRecipe(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        queryset=models.Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select meal tag"
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=models.Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select existing ingredients"
    )


    class Meta:
        model = models.Recipe
        fields = ['title', 'description', 'slug', 'instructions', 'ingredients', 'banner', 'meal_type', 'tags']
        widgets = {
            'ingredients': forms.SelectMultiple(attrs={
                'class': 'ingredient-selector',
                'data-add-url': reverse_lazy('admin:recipes_ingredient_add')
            }),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = models.RecipeRating
        fields = ['rating']
        widgets = {
            'rating': forms.HiddenInput()  # We'll handle this with stars
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.RecipeComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }