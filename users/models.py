
# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('chef', 'Chef'),
        ('customer', 'Customer'),
    )
    username=models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, blank=True, null=True, default=None)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def clean(self):
        super().clean()
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': 'This email is already in use.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.is_superuser and not self.user_type:
            self.user_type = None
        super().save(*args, **kwargs)

    def get_username(self):
        return self.username

    
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    













# class User(AbstractUser):
#     USER_TYPES = (
#         ('chef', 'Chef'),
#         ('customer', 'Customer'),
#     )
#     username=models.CharField(max_length=50, unique=True)
#     user_type = models.CharField(max_length=10, choices=USER_TYPES)
#     profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
#     bio = models.TextField(blank=True)
#     phone_number = models.CharField(max_length=15, blank=True)

#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         help_text='The groups this user belongs to.',
#         related_name="custom_user_groups",  # Unique related_name
#         related_query_name="user",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_name="custom_user_permissions",  # Unique related_name
#         related_query_name="user",
#     )
    
#     def __str__(self):
#         return f"{self.username} ({self.get_user_type_display()})"
    
