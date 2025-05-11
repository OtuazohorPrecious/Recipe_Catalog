from django.urls import path
from .views import (CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, 
CustomPasswordResetCompleteView, profile, profile_edit, register_view, login_view, logout_view, chef_profile)

app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    
]



urlpatterns += [
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-confirm/<uidb64>/set-password/', 
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', 
         CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    

    path('profile/', profile, name='profile'),
    path('chef/<str:username>/', chef_profile, name='chef_profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
]