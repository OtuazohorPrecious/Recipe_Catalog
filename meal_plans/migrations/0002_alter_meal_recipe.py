# Generated by Django 5.1.7 on 2025-04-06 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal_plans', '0001_initial'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='recipes.recipe'),
        ),
    ]
