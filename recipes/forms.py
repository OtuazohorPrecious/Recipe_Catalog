from django import forms
from . import models

from django.core.exceptions import ValidationError
from django.urls import reverse_lazy





class createRecipe(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        queryset=models.Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select meal tag"
    )
    

    class Meta:
        model = models.Recipe
        fields = ['title', 'description', 'slug', 'instructions', 'ingredients_list', 'banner', 'estimated_calories', 'servings', 'meal_type', 'tags']
        

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