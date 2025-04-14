# meal_plans/urls.py
from django.urls import path
from . import views

app_name = 'meal_plans'

urlpatterns = [
    path('', views.meal_plans_list, name='list'),
    path('create/', views.create_meal_plan, name='create_meal_plan'),
    path('<int:meal_plan_id>/select-meals/', views.select_meals, name='select_meals'),
    path('<int:meal_plan_id>/', views.view_meal_plan, name='view_meal_plan'),
    path('<int:meal_plan_id>/edit/', views.select_meals, name='edit_meal_plan'),
    path('<int:meal_plan_id>/delete/', views.meal_plan_delete, name='delete'),
]