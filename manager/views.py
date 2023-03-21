from django.shortcuts import render , redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, DocumentForm, AddNewUser
from .models import Document, Company, Entity, Investing, Right, User
from manager.utils import airtable

from django.contrib.auth import authenticate , login
from django.contrib import messages
import pandas as pd
import django.core.files
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth import logout



# Create your views here.

def home(request):

    return render(request, 'home.html')



def log_out(request): #logs out the user and redirects to home page
    logout(request)
    return redirect('log_in')


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

# @login_required
def dashboard(request):
    context = {
    }
    return render(request, 'dashboard.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Entity, Company

# @login_required
def entity_view(request, name):
    entity = get_object_or_404(Entity, name=name)

    return render(request, 'entity_details.html', {'entity': entity})

# @login_required
def company_view(request, name):

    company = get_object_or_404(Company, name=name)

    return render(request, 'company_details.html', {'company': company})

# @login_required
def entities(request):
    investingCompanies = Entity.objects.all()
    context = {
    'data' : investingCompanies
    }
    return render(request, 'entities.html', context)

# @login_required
def sync(request):
    if request.method == 'POST':
        airtable.update_all()
        return redirect(dashboard)

    return redirect(dashboard)

def founders(request):
    foundingCompanies = Entity.objects.all()
    context = {
    'data' : foundingCompanies
    }
    return render(request, 'founders.html', context)

def error_404(request, exception):
    return render(request, '404.html')

# @login_required
def portfolio(request):
    portfolioCompanies = Company.objects.filter(wayra_investment__gt=0) #.filter(wayra_investment!=0) #.order_by('date')
    context = {
        'data' : portfolioCompanies,
    }
    return render(request, 'portfolio.html', context)

# @login_required
def ecosystem(request):
    ecosystemCompanies = Company.objects.filter(wayra_investment=0) #.filter(wayra_investment==0) #.order_by('date')
    context = {
        'data' : ecosystemCompanies,
    }
    return render(request, 'ecosystem.html', context)

# @login_required
#@user_passes_test(admin_test, login_url='adminProhibitted')
def users(request):
    allUsers = User.objects.all().filter(user_type=1) #.exclude(id=request.user.id).order_by('id')
    context = {
        'data' : allUsers,
    }
    print(allUsers)
    return render(request, 'users.html', context)

#@login_required
#@user_passes_test(admin_test, login_url='adminProhibitted')
def adminAddUser(request):
    if request.method == 'POST':
        form = AddNewUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New User added successfully.')
            form = AddNewUser()
        # if errors, show error message
        # messages.add_message(request, messages.ERROR, "There are some errors.")
    else:
        form = AddNewUser()
    context = {
        'form': form
    }
    return render(request, 'admin_add_user.html', context)

#@login_required
#@user_passes_test(admin_test, login_url='adminProhibitted')
def adminEditUser(request, userID):
    account = User.objects.get(id=userID)
    if request.method == 'POST':
        form = AddNewUser(request.POST, instance=account)
        if form.is_valid():
            account.first_name = form.cleaned_data.get('first_name')
            account.last_name = form.cleaned_data.get('last_name')
            account.username = form.cleaned_data.get('email')
            account.email = form.cleaned_data.get('email')
            account.save()
            account.set_password(form.cleaned_data.get('password'))
            account.save()
            messages.success(request, 'User updated successfully.')
            form = AddNewUser(initial={'first_name': account.first_name, 'last_name': account.last_name, 'email': account.email})
            # return redirect('directorViewTerms')
    else:
        form = AddNewUser(initial={'first_name': account.first_name, 'last_name': account.last_name, 'email': account.email})
    context = {
        'form': form,
        'account': account,
    }

    return render(request, 'admin_edit_user.html', context)

#@login_required
#@user_passes_test(admin_test, login_url='adminProhibitted')
def adminDeleteUser(request, userID):
    account = User.objects.get(id=userID)
    account.delete()
    return HttpResponseRedirect(reverse('users'))

# @login_required
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
            dat = df.iloc[1,1]
            # Company.objects.all().delete()
            # Entity.objects.all().delete()
            # Investing.objects.all().delete()
            #return HttpResponse(str(dat))
            #return HttpResponse(str(df.shape[0]))
            for x in range(df.shape[0]):
                name = df.iloc[x, 0]
                registeredNumber = df.iloc[x, 1]
                countryCode = df.iloc[x, 2]


                #return HttpResponse(str(Entity.objects.count()))
                #return HttpResponse(str(Company.objects.filter(name = name).filter(number = registeredNumber).count() == 0))
                if Company.objects.filter(name = name).filter(number = registeredNumber).count() == 0:
                    company = Company.objects.create(name = name, number = registeredNumber, country_code = countryCode)
                    corps = Company.objects.filter(name = name).first()
                    investorList = df.iloc[x, 3].split(",")
                    #return HttpResponse(str(investorList))
                    Investors = []
                    Amounts = []
                    for i in range(len(investorList)):
                        if i % 2 == 0:
                            Amounts.append(investorList[i])
                        else:
                            Investors.append(investorList[i])

                    for i in range(0, len(investorList), 2):
                        #investor list contains[name, amount, name, amount...]
                        #make sure to alternate elements for name and amount. And feed them in their respective areas.
                        try:
                            #return HttpResponse(investorList[i])
                            investorEntity = Entity.objects.get(name = investorList[i])
                            Investor = Investing.objects.create(investor = investorEntity, company = company, amount = float(investorList[i+1]))
                            Investor.save()
                            company.investors.add(investorEntity)
                            #add this investor to created company
                        except Entity.DoesNotExist:
                            investorEntity = Entity.objects.create(name = investorList[i])
                            Investor = Investing.objects.create(investor = investorEntity, company = company, amount = float(investorList[i+1]))
                            investorEntity.save()
                            Investor.save()
                            company.investors.add(investorEntity)
                            company.save()
                            #create + add this investor to created company(entity of investor, )
                        Investors.append(Investor)

                        company.investors.add(investorEntity)


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
                            company.save()
                            #return HttpResponse("Banana")
                            Founders.append(founder)
                            #add this investor to created company
                        except Entity.DoesNotExist:
                            #return HttpResponse("banana")
                            founder = Entity.objects.create(name = founderName)

                            founder.founding_company.add(company)
                            #founder.invested_company.add(company, 900) #<- work on this aspect.

                            company.founders.add(founder)
                            Founders.append(founder)
                            founder.save()
                            company.save()
                            #create + add this investor to created company

                        #return HttpResponse(Entity.objects.count())
                        #return HttpResponse(Company.objects.filter(name=name).first().name)

                    rightsList = df.iloc[x, 5].split(",")

                    for right in rightsList:
                        try:
                            validRight = Right.objects.get(name=right)
                            validRight.holding_right.add(company)
                            validRight.save()
                        except Right.DoesNotExist:
                            validRight = Right.objects.create(name=right)
                            validRight.holding_right.add(company)
                            validRight.save()


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
            #return HttpResponse("The number of entities is: " + str(Entity.objects.get(name="Also")))
            return redirect("portfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = DocumentForm() #A empty, unbound form
        return render(request, 'addCompany.html', {'form': form})
