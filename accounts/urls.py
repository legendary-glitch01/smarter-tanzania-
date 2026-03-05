from django.urls import path, include
from .views import home_view, login_view, register_view, logout_view, user_profile_view, GoogleLogin, AppleLogin, UserProfileView

# This MUST be named exactly 'urlpatterns'
urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login_page'),
    path('register/', register_view, name='register_page'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile_view, name='user_profile'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/apple/', AppleLogin.as_view(), name='apple_login'),
    path('api/profile/', UserProfileView.as_view(), name='api_user_profile'),
]