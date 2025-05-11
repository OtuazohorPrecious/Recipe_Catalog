from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'recipes'

urlpatterns = [
    path('', views.recipes_list, name='list'),
    path('new-recipe/', login_required(views.recipe_new), name='new-recipe'),
    path('add_meal_tag/', views.add_meal_tag, name='add_meal_tag'),
    path('<slug:slug>', views.recipe_page, name='page'),
    path('search/', views.recipe_search, name='recipe_search'),
    path('<slug:slug>/edit/', views.recipe_edit, name='edit'),
    path('<slug:slug>/delete/', views.recipe_delete, name='delete'),
    path('<slug:slug>/rate/', views.rate_recipe, name='rate-recipe'),
    path('<slug:slug>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
]
