from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import LoginForm, UploadFileForm
from django.contrib.auth import authenticate , login
from django.contrib import messages
import pandas as pd


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


#add view(s) to add companies to portfolio.
def addCompany(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excelFile = request.FILES['file']
            #use pandas to read excelFile
            df = pd.readExcel(excelFile, dtype = {'Name':'string', 'Number':'string', 'Country':'string', 'Investors': 'string', 'Founders': 'string', 'Rights': 'string'})
            for x in range(df.shape[0]):
                name = df[x, 0]
                registeredNumber = df[x, 1]
                countryCode = df[x, 2]
                company = Company.objects.create(name = name, number = registeredNumber, country_code = countryCode)
                investorList = df[x, 3].split(",")
                Investors = []
                for investorName in investorList:
                    try:
                        investor = Entity.objects.get(name = investorName)
                        #add this investor to created company
                    except Entity.DoesNotExist:
                        investor = Entity.objects.create(name = y)
                        #create + add this investor to created company
                    Investors.append(investor)
                    company.objects.investors.add(investor)

                founderList = df[x, 4].split(",")
                Founders = []
                for founderName in founderList:
                    try:
                        founder = Entity.objects.get(name = founderName)
                        #add this investor to created company
                    except Entity.DoesNotExist:
                        founder = Entity.objects.create(name = y)
                        #create + add this investor to created company
                    Founders.append(founder)
                    company.object.investors.add(founder)
                rightsList = df[x, 5].split(",")
                rights = Right.objects.filter(name in rightsList)
                company.objects.wayra_right.add(rights)
                Company.save()
                #company = Company.objects.create(name = name, number = registeredNumber, country_code = countryCode)

                    
            #Columns 1-3 for each row should be fairly straightforward. (df = pd.readExcel(excelFile), then use df[0] to iterate through every row.)
            #for Column 4, create an entity object with this company name as "company", their name as investor, and the amount as the amount.
            #for Column 5, create an entity with this company as "founding company" and their name as "invested company"
            #for Column 6, make a list out of the mentioned rights and say Right.objects.filter(name in WhateverICallMyList) to return a querySet.
            #return excel.make_response(filehandle.get_sheet(), "csv")
            return redirect(company_view)
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
        return render(request, 'addCompany.html', {'form': UploadFileForm()})