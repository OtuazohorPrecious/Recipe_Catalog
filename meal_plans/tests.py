from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from .models import MealPlan, Day, Meal

User = get_user_model()

class MealPlanModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='planuser', email='planuser@gmail.com', password='test123')
        cls.recipe = Recipe.objects.create(
            title='Plan Recipe',
            ingredients_list='test',
            created_by=cls.user
        )
        
    def test_meal_plan_creation(self):
        plan = MealPlan.objects.create(
            start_date='2023-01-01',
            end_date='2023-01-07',
            user_id=self.user.id
        )
        day = Day.objects.create(
            date='2023-01-01',
            meal_plan=plan
        )
        meal = Meal.objects.create(
            day=day,
            meal_type='breakfast',
            recipe=self.recipe
        )
        
        self.assertEqual(plan.days.count(), 1)
        self.assertEqual(day.meals.count(), 1)
        self.assertEqual(day.get_total_calories(), self.recipe.estimated_calories)

class MealPlanViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            title='Plan View Recipe',
            ingredients_list='test',
            created_by=self.user
        )
        
    def test_meal_plan_create_view(self):
        response = self.client.post(reverse('meal_plans:create_meal_plan'), {
            'start_date': '2023-01-01',
            'end_date': '2023-01-07'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MealPlan.objects.filter(user_id=self.user.id).exists())

    def test_meal_selection_view(self):
        plan = MealPlan.objects.create(
            start_date='2023-01-01',
            end_date='2023-01-01',
            user_id=self.user.id
        )
        day = Day.objects.create(
            date='2023-01-01',
            meal_plan=plan
        )
        
        response = self.client.post(reverse('meal_plans:select_meals', args=[plan.id]), {
            f'day_{day.id}_meal_breakfast': self.recipe.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(day.meals.first().recipe, self.recipe)