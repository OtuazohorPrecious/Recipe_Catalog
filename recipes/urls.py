from django.urls import path
from . import views


app_name = 'recipes'

urlpatterns = [
    path('', views.recipes_list, name='list'),
    path('new-recipe/', views.recipe_new, name='new-recipe'),
    path('<slug:slug>', views.recipe_page, name='page'),
    path('search/', views.recipe_search, name='recipe_search'),
]
