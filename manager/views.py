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
