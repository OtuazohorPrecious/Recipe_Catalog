from django import forms
from . import models

from django.core.exceptions import ValidationError

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
    )
    class Meta:
        model = models.Recipe
        fields = ['title', 'description', 'slug', 'instructions', 'banner', 'meal_type', 'tags']