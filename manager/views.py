from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return HttpResponse("Hello, home page here please.")
    
def login(request):
    return render(request, 'login.html')
 