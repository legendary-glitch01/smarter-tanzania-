# In chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required # This forces the user to log in first
def chat_home(request):
    return render(request, 'chat/chat.html')