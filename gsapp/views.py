from django.shortcuts import render

def home(request):
    return render(request, 'gsapp/home.html')

def success(request):
    return render(request, 'gsapp/success.html')

