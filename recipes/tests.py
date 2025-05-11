from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Recipe, Tag, RecipeRating

User = get_user_model()

class RecipeModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='recipeuser',email='recipeuser@gmail.com', password='test123')
        cls.tag = Tag.objects.create(name='Test Tag')
        
    def test_recipe_creation(self):
        recipe = Recipe.objects.create(
            title='Test Recipe',
            ingredients_list='chicken, rice',
            instructions='Cook it',
            created_by=self.user,
            slug='test-recipe'
        )
        recipe.tags.add(self.tag)
        
        self.assertEqual(recipe.slug, 'test-recipe')
        self.assertEqual(recipe.tags.count(), 1)
        self.assertIsNotNone(recipe.created_at)



    def test_calorie_estimation(self):
        recipe = Recipe.objects.create(
            title='Calorie Test',
            ingredients_list='200g chicken, 100g rice',
            created_by=self.user
        )
        self.assertIsNotNone(recipe.estimated_calories)
        self.assertGreater(recipe.estimated_calories, 0)

class RecipeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            title='View Test',
            ingredients_list='test',
            instructions='test',
            created_by=self.user,
            slug='slug'
        )

    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View Test')

    def test_recipe_create_view(self):
        self.user = User.objects.create_user(username='newuser', email='newuser@gmail.com', password='newpass')
        self.client.login(username='newuser', password='newpass')
        response = self.client.post(reverse('recipes:new-recipe'), {
            'title': 'New Test Recipe',
            'ingredients_list': 'test ingredients',
            'instructions': 'test instructions',
            'tags': 'vegetarian',
            'slug': 'slug',
            'description': 'test description',
            'meal_type': 'Breakfast',
            'estimated_calories':790,
            'servings': 2,
        })
        print("Response status code:", response.status_code)
        if response.status_code != 302:
            print("Response content:", response.content)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(title='New Test Recipe').exists())

    def test_recipe_rating(self):
        response = self.client.post(reverse('recipes:rate-recipe', args=[self.recipe.slug]), {
            'rating': 5
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.recipe.ratings.first().rating, 5)