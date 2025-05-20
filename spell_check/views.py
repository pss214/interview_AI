from django.shortcuts import render
from django.contrib import messages
from spell_check.spell_checker import SpellChecker

def index(request):
    user_input = ''
    if request.method == 'POST':
        checker = SpellChecker()
        user_input = request.POST.get('text', '').strip()
        result = checker.spell_check(user_input)
        messages.success(request, result)
    
    return render(request, 'spellcheck.html', {'user_input': user_input})
