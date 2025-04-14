from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, UserChangeForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    username=forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPES, widget=forms.RadioSelect)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                 'user_type', 'profile_picture', 'password1', 'password2']
        

class UserUpdateForm(UserChangeForm):
    password = None  
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'bio', 'phone_number']