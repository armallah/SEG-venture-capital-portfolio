from django.shortcuts import render , redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, DocumentForm
from .models import Document, Company, Entity, Investing, Right
from django.contrib.auth import authenticate , login
from django.contrib import messages
import pandas as pd
import django.core.files


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

def entities(request):
    context = {

    }
    return render(request, 'entities.html', context)

def founders(request):
    context = {

    }
    return render(request, 'founders.html', context)

def error_404(request, exception):
    return render(request, '404.html')

def portfolio(request):
    context = {
    }
    return render(request, 'portfolio.html', context)

def ecosystem(request):
    context = {
    }
    return render(request, 'ecosystem.html', context)


#add view(s) to add companies to portfolio.
def addCompany(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #convert from model form to regular form.
            filename = str(request.FILES)

            #print("banana")
            #spreadsheet = Document.upload.path
            df = pd.read_excel(request.FILES['upload'], dtype = {'Name':'string', 'Number':'string', 'Country':'string', 'Investors': 'string', 'Founders': 'string', 'Rights': 'string'})
            #dat = df.shape
            dat = df.iloc[0,1]
            #return HttpResponse(str(dat))
            for x in range(df.shape[0]):
                name = df.iloc[x, 0]
                registeredNumber = df.iloc[x, 1]
                countryCode = df.iloc[x, 2]
                #return HttpResponse(str(Company.objects.count()))
                Company.objects.all().delete()
                Entity.objects.all().delete()
                #return HttpResponse(str(Company.objects.filter(name = name).filter(number = registeredNumber).count() == 0))
                if Company.objects.filter(name = name).filter(number = registeredNumber).count() == 0:
                    company = Company.objects.create(name = name, number = registeredNumber, country_code = countryCode)
                    corps = Company.objects.filter(name = name).first()
                    investorList = df.iloc[x, 3].split(",")
                    Investors = []
                    """
                    for investorName in investorList:
                        #investor list contains[name, amount, name, amount...]
                        #make sure to alternate elements for name and amount. And feed them in their respective areas.
                        try:
                            investor = Investing.objects.get(investor = investorName)
                            #add this investor to created company
                        except Entity.DoesNotExist:
                            investor = Investing.objects.create(investor = investorName, company = name, amount = )
                            #create + add this investor to created company(entity of investor, )
                        Investors.append(investor)
                        company.investors.add(investor)
                    """
                    founderList = df.iloc[x, 4].split(",")
                    #return HttpResponse(str(founderList))
                    founder1 = Entity.objects.count()
                    #Company.objects.all().delete()
                    #Entity.objects.all().delete()
                    #return HttpResponse(str(Entity.objects.count()))
                    #return HttpResponse(str(Company.objects.count()))
                    Founders = []
                    for founderName in founderList:
                        #instead of try/except, make the Entity.objects.get(name = founderName) first, and if the size is zero, make a new Entity.(Definitely this!)
                        try:
                            founder = Entity.objects.get(name = founderName)
                            company.founders.add(founder)
                            return HttpResponse(founderName)
                            Founders.append(founder)
                            #add this investor to created company
                        except Entity.DoesNotExist:
                            #return HttpResponse("banana")
                            founder = Entity.objects.create(name = founderName)
                            company.founders.add(founder)
                            Founders.append(founder)
                            founder.save()
                            #create + add this investor to created company

                        #return HttpResponse(Entity.objects.count())
                        #return HttpResponse(Company.objects.filter(name=name).first().name)

                    rightsList = df.iloc[x, 5].split(",")
                    defaultQuery = Right.objects.filter(name="Bananarama")
                    for right in rightsList:
                        validRights = Right.objects.filter(name=right)
                        defaultQuery = defaultQuery | validRights
                    #rights = Right.objects.filter(5 == 2)
                    #company.wayra_right.add(defaultQuery)
                    company.save()


                #company = Company.objects.create(name = name, number = registeredNumber, country_code = countryCode)


            #Columns 1-3 for each row should be fairly straightforward. (df = pd.readExcel(excelFile), then use df[0] to iterate through every row.)
            #for Column 4, create an entity object with this company name as "company", their name as investor, and the amount as the amount.
            #for Column 5, create an entity with this company as "founding company" and their name as "invested company"
            #for Column 6, make a list out of the mentioned rights and say Right.objects.filter(name in WhateverICallMyList) to return a querySet.
            #return excel.make_response(filehandle.get_sheet(), "csv")
            #compQuery = Company.objects.all().get(id=45)
            #return HttpResponse(str(compQuery) + str(Company.objects.all().count()))
            #print("spreadsheet")
            #Company.objects.all().delete()
            #return HttpResponse(str(Entity.objects.count()))
            #return HttpResponse(str(Entity.objects.get(name="Mom")))
            return redirect("portfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = DocumentForm() #A empty, unbound form
        return render(request, 'addCompany.html', {'form': form})
