from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'core/index.html')

def categories(request):
    return render(request, 'core/categories.html')

def category(request):
    return render(request, 'core/category.html')

def login(request):
    return render(request, 'core/login.html')

def signup(request):
    return render(request, 'core/signup.html')
