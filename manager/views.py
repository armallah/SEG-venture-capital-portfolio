from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate , login
from django.contrib import messages

# Create your views here.

def home(request):
    return HttpResponse("Hello, home page or not here.")    
    
def log_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
            
    form = LoginForm()
    return render(request, 'login.html' , {'form':form})
 
def dashboard(request):
    context = {
    }
    return render(request, 'dashboard.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Entity, Company

    
def entity_view(request, name):
    entity = get_object_or_404(Entity, name=name)
    
    return render(request, 'entity_details.html', {'entity': entity})


def company_view(request, name):
    
    company = get_object_or_404(Company, name=name)
    
    return render(request, 'company_details.html', {'company': company})

def error_404(request, exception):
    return render(request, '404.html')

def portfolio(request):
    context = {
    }
    return render(request, 'portfolio.html', context)

def company_founders(request, company_name):
    company = get_object_or_404(Company, name=company_name)
    context = {'company': company}
    
    return render(request, 'founders_details.html', context)


def company_investors(request, company_name):
    company = get_object_or_404(Company, name=company_name)
    context = {'company': company}
    
    return render(request, 'investors_details.html', context)



