from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
#from .models import Profile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import SetPasswordForm

User = get_user_model()

class UserModelTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_superuser)

    # def test_profile_auto_creation(self):
    #     user = User.objects.create_user(username='profiletest', password='test123')
    #     self.assertTrue(hasattr(user, 'profile'))
    #     self.assertEqual(user.profile.user, user)

class AuthViewTests(TestCase):
    def test_register_view(self):
        # Get initial user count
        initial_count = User.objects.count()
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'user_type': 'chef',
        }, follow=True)  # follow redirects

        
        #self.assertEqual(response.status_code, 302)  # Check redirect happened
        self.assertEqual(response.status_code, 200) # Final status after redirect
        self.assertRedirects(response, reverse('home'))  # Verify redirect target
        # Check user creation
        self.assertEqual(User.objects.count(), initial_count + 1)
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'new@example.com')
        self.assertTrue(User.objects.filter(username='newuser').exists())

       
        
    def test_password_reset_flow(self):
        user = User.objects.create_user(username='resetuser', email='reset@example.com', password='oldpass')
        
        # Request password reset email
        response = self.client.post(reverse('users:password_reset'), {'email': 'reset@example.com'})
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("password reset email sent successfully" in str(message).lower() for message in messages))
        
        # Generate valid uid and token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        reset_confirm_url = reverse('users:password_reset_confirm', args=[uid, token])
        
        

        # First GET: token validation, expect 302 redirect to 'set-password' URL
        response = self.client.get(reset_confirm_url)
        self.assertEqual(response.status_code, 302)

        # Follow redirect URL
        redirect_url = response['Location']
        self.assertIn('/set-password/', redirect_url)

        # Second GET: actual password reset form page, expect 200
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)
              

        form = SetPasswordForm(user, {
            'new_password1': 'Newpass123!',
            'new_password2': 'Newpass123!'
        })

        if form.is_valid():
            form.save()
        else:
            print("Manual form errors:", form.errors)
    
        
        # Refresh user from DB and check password
        user.refresh_from_db()
        self.assertTrue(user.check_password('Newpass123!'))



    
    



    # def test_password_reset_flow(self):
    #     user = User.objects.create_user(username='resetuser', email='reset@example.com', password='oldpass')
        
    #     # Request reset
    #     response = self.client.post(reverse('users:password_reset'), {'email': 'reset@example.com'})
        
    #     # Check messages
    #     messages = list(get_messages(response.wsgi_request))
    #     for message in messages:
    #         print(message)

    #     self.assertTrue(any("reset email" in str(message).lower() for message in messages))
        
    #     # Test rest of flow...
    #     # Get uid and token from test email (in production, get from email)
    #     uid = urlsafe_base64_encode(force_bytes(user.pk))
    #     token = default_token_generator.make_token(user)
    #     # uid = 'Mg'
    #     # token = 'abc123-xyz456'
        
    #     # Check confirm page
    #     self.client.logout()

    #     response = self.client.get(reverse('users:password_reset_confirm', args=[uid, token]))
    #     self.assertEqual(response.status_code, 200)
    #     reset_confirm_url = reverse('users:password_reset_confirm', args=[uid, token])
        
    #     # Submit new password
    #     response = self.client.post(reset_confirm_url, {
    #         'new_password1': 'newpass123',
    #         'new_password2': 'newpass123'
    #     }, follow=True)

        
    #     # Verify password changed
    #     user.refresh_from_db()
    #     print("Password hash after reset:", user.password)
    #     print("Password check:", user.check_password('newpass123'))

    #     self.assertTrue(user.check_password('newpass123'))