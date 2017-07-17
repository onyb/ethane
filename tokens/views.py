from django.shortcuts import render

def token_distribution(request):
    return render(request, 'tokens/token_distribution.html')
