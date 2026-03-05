import json
import os
import google.generativeai as genai
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from dotenv import load_dotenv
from .models import ChatSession, Message

# Load environment
load_dotenv(os.path.join(settings.BASE_DIR, '.env'))

SYSTEM_INSTRUCTION = "You are EDU-TZ AI, a Tanzanian education expert made by christian allan. Provide NECTA syllabus help in Swahili and English."

def get_edu_brain_model():
    """
    STRICT PRIORITY: We force the use of 1.5-flash because it has 
    the highest free tier quota (15 requests per minute).
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return None
    
    try:
        genai.configure(api_key=api_key)
        
        # We search specifically for the 'flash' model first
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priority list
        preferred_order = [
            'models/gemini-1.5-flash', 
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-pro'
        ]
        
        selected = None
        for p in preferred_order:
            if p in available_models:
                selected = p
                break
        
        if not selected:
            selected = available_models[0] # Fallback to first available

        print(f"✅ EDU-TZ Success: Forced Model to '{selected}'")
        return genai.GenerativeModel(model_name=selected)

    except Exception as e:
        print(f"❌ Critical Init Error: {e}")
        return None

@login_required
def chat_home(request):
    session, _ = ChatSession.objects.get_or_create(user=request.user)
    messages = Message.objects.filter(session=session).order_by('timestamp')
    return render(request, 'chat/chat.html', {'messages': messages, 'user': request.user})

@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_text = data.get('message')
            session, _ = ChatSession.objects.get_or_create(user=request.user)

            if not user_text:
                return JsonResponse({'success': False, 'error': 'Message empty'})

            Message.objects.create(session=session, sender='user', text=user_text)

            model = get_edu_brain_model()
            if not model:
                return JsonResponse({'success': False, 'error': "API Key Offline."})

            # AI CALL
            full_prompt = f"{SYSTEM_INSTRUCTION}\n\nStudent: {user_text}"
            response = model.generate_content(full_prompt)
            
            ai_text = response.text
            Message.objects.create(session=session, sender='ai', text=ai_text)

            return JsonResponse({'success': True, 'ai_message': {'text': ai_text}})

        except Exception as e:
            error_str = str(e)
            # Custom message for Quota (429)
            if "429" in error_str:
                return JsonResponse({
                    'success': False, 
                    'error': "⚠️ Rate Limit Reached: The AI is busy. Please wait 60 seconds and try again. (Google Free Tier limitation)"
                })
            return JsonResponse({'success': False, 'error': f"EDU-TZ AI Error: {error_str}"})

    return JsonResponse({'success': False, 'error': 'Invalid request'})