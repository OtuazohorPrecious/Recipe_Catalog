from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import UserRegistrationForm, UserUpdateForm
from django.urls import reverse_lazy
from recipes.models import Recipe
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.messages import constants as messages_constants
from django.contrib.auth.forms import SetPasswordForm

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the new user first
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Then login the user instance
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', { "form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("recipes:list")
        else:
            messages.error(request, "❌ Username and password mismatch")

    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', { "form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("recipes:list")
    




# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'users/register.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        
        # Check if email exists
        if not User.objects.filter(email=email).exists():
            messages.error(request, "❌ No account found with this email address")
            return render(request, self.template_name, {'email': email})
        
        # If email exists, proceed normally
        messages.add_message(request, messages_constants.SUCCESS, "Password reset email sent successfully!")
        return super().post(request, *args, **kwargs)
    

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    form_class = SetPasswordForm # Explicitly set the form class

    # def get_form_class(self):
    #     print("Using form class:", super().get_form_class())
    #     return super().get_form_class()

    def form_valid(self, form):
        print("form_valid called")
        user = form.save()
        print(f"Password changed for user: {user.username}")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        print("POST received in password reset confirm view")
        form = self.get_form()
        print("Form is valid?", form.is_valid())
        print("Form errors:", form.errors)
        return super().post(request, *args, **kwargs)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})


def chef_profile(request, username):
    chef = get_object_or_404(User, username=username)
    public_recipes = Recipe.objects.filter(
        created_by=chef
    )  
    
    context = {
        'chef': chef,
        'recipes': public_recipes,
        'recipe_count': public_recipes.count(),
        # Add more public stats as needed
    }
    return render(request, 'users/chef_profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})