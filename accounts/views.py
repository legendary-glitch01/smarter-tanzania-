from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import User, Profile
from .serializers import ProfileSerializer

# Classes...
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

def home_view(request):
    # If they are already logged in, send them to chat immediately
    if request.user.is_authenticated:
        return redirect('chat_dashboard') 
    return render(request, 'accounts/home.html')

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('chat_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Ensure user has a profile before logging in
            try:
                user.profile
            except Profile.DoesNotExist:
                Profile.objects.create(user=user, registration_method='email')
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('chat_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')

@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('chat_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'All fields are required')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'accounts/register.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            return render(request, 'accounts/register.html')
        
        # Create user (Profile is auto-created by signal)
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Ensure profile was created
        try:
            user.profile
        except Profile.DoesNotExist:
            Profile.objects.create(user=user, registration_method='email')
        
        # Log them in
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('chat_dashboard')
    
    return render(request, 'accounts/register.html')

@login_required(login_url='login_page')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('landing_page')

@login_required(login_url='login_page')
def user_profile_view(request):
    """Display user profile with account details"""
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })