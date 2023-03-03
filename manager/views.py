from django.shortcuts import render

# Create your views here.
def dashboard(request):
    context = {
    }
    return render(request, 'dashboard.html', context)

def portfolio(request):
    context = {
    }
    return render(request, 'portfolio.html', context)

def entities(request):
    context = {
    }
    return render(request, 'entities.html', context)

def founders(request):
    context = {
    }
    return render(request, 'founders.html', context)
