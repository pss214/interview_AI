# chatbot/views.py
import json
from django.http import JsonResponse
from django.shortcuts import render

from chatbot.answer_ai import evaluate_answer, get_job_question, get_me_question

def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        job = data.get('job')
        count = data.get('count')
        if job == None:
            result = "직업 없음"
            return JsonResponse({'response':result},status=400)
        if text=="질문":
            if count<3:
                result = get_me_question()
            else:
                result = get_job_question(job)
            return JsonResponse({'response': result}, status=200)
        if text:
            result = evaluate_answer(text,job)
            return JsonResponse({'response': result}, status=200)
    return render(request, 'chat.html')
    