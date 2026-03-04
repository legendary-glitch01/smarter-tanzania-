from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view # Your Landing Page view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')), # This is where the Gemini page lives
    path('social/', include('allauth.urls')),
    
    # This makes the Landing Page the FIRST thing people see
    path('', home_view, name='landing_page'), 
]