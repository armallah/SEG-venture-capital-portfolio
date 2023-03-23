from django.shortcuts import render , redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
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

def admin_test(user): # checks if user is an admin
    return (user.user_type == 2)

def adminProhibitted(request):
    return render(request, 'adminProhibitted.html')

def home(request):

    return render(request, 'home.html')



def log_out(request): #logs out the user and redirects to home page
    logout(request)
    return redirect('home')


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
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

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


            df = pd.read_excel(request.FILES['upload'], dtype = {'Name':'string', 'Number':'string', 'Country':'string', 'Investors': 'string', 'Founders': 'string', 'Rights': 'string', 'Wayra Investment': 'float', 'Description': 'string'})

            Company.objects.all().delete()
            Entity.objects.all().delete()
            Investing.objects.all().delete()
            Right.objects.all().delete()

            for x in range(df.shape[0]):
                name = df.iloc[x, 0].strip()
                registeredNumber = df.iloc[x, 1].strip()
                countryCode = df.iloc[x, 2].strip()
                wayraInvestment = 0
                if not pd.isna(df.iloc[x, 6]):
                        wayraInvestment = df.iloc[x, 6]
                description = "No description"
                if not pd.isna(df.iloc[x, 7]):
                        description = df.iloc[x, 7].strip()

                if Company.objects.filter(name = name).filter(number = registeredNumber).count() == 0:
                    company = Company.objects.create(name = name, number = registeredNumber, country_code = countryCode, wayra_investment = wayraInvestment, description = description)

                    investorList = df.iloc[x, 3].split(",")


                    for i in range(0, len(investorList), 2):
                        #investor list contains[name, amount, name, amount...]
                        #make sure to alternate elements for name and amount. And feed them in their respective areas.
                        investorName = investorList[i].strip()
                        try:
                            investorEntity = Entity.objects.get(name = investorName)
                            Investor = Investing.objects.create(investor = investorEntity, company = company, amount = float(investorList[i+1]))
                            Investor.save()
                            company.investors.add(investorEntity)
                            #add this investor to created company
                        except Entity.DoesNotExist:
                            investorEntity = Entity.objects.create(name = investorName)
                            Investor = Investing.objects.create(investor = investorEntity, company = company, amount = float(investorList[i+1]))
                            investorEntity.save()
                            Investor.save()
                            company.investors.add(investorEntity)
                            company.save()


                        company.investors.add(investorEntity)


                    founderList = df.iloc[x, 4].split(",")


                    for founderName in founderList:
                        try:
                            founder = Entity.objects.get(name = founderName.strip())
                            company.founders.add(founder)
                            company.save()

                        except Entity.DoesNotExist:
                            founder = Entity.objects.create(name = founderName.strip())

                            founder.founding_company.add(company)

                            company.founders.add(founder)
                            founder.save()
                            company.save()



                    rightsList = ""
                    if not pd.isna(df.iloc[x, 5]):
                        rightsList = df.iloc[x, 5].split(",")

                    for right in rightsList:
                        cleanRight = right.strip()
                        try:
                            validRight = Right.objects.get(name=cleanRight)
                            validRight.holding_right.add(company)
                            validRight.save()
                        except Right.DoesNotExist:
                            validRight = Right.objects.create(name=cleanRight)
                            validRight.holding_right.add(company)
                            validRight.save()
                    company.save()
            Document.objects.all().delete()
            return redirect("portfolio")
        else:
            return render(request, 'addCompany.html', {'form': form, 'error':'Please upload a .xlsx file.'})
    else:
        form = DocumentForm() #A empty, unbound form
        return render(request, 'addCompany.html', {'form': form})

# @login_required
#add view(s) to add companies to portfolio.
def addCompanyOne(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        #Company.objects.all().delete()
        #Entity.objects.all().delete()
        #Investing.objects.all().delete()
        #Right.objects.all().delete()
        if form.is_valid():
            Name = form.data['name']
            
            Number = form.data['number']
            if Company.objects.filter(number=Number).count() > 0:
                return render(request, 'addCompanyOne.html', {'form': form, 'error': 'There already exist a company with this Wayra number.'})
            Country = form.data['country_code']
            WayraInvestment = form.data['wayra_investment']
            Description = form.data['description']
            FounderName = form.data['founderName']
            try:
                founder = Entity.objects.get(name=FounderName)
            except Entity.DoesNotExist:
                founder = Entity.objects.create(name=FounderName)
            newCompany = Company.objects.create(name=Name, number=Number, country_code=Country, wayra_investment=WayraInvestment, description=Description)
            newCompany.founders.add(founder)
            #Entity.objects.create(name="John Doe").founding_company.add(newCompany)
            newCompany.save()
            return redirect("portfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = CompanyForm() #A empty, unbound form
        return render(request, 'addCompanyOne.html', {'form': form})

# @login_required
#add view(s) to add companies to portfolio.
def addFounderOne(request):
    if request.method == 'POST':
        form = FounderForm(request.POST)
        #Company.objects.all().delete()
        #Entity.objects.all().delete()
        #Investing.objects.all().delete()
        #Right.objects.all().delete()
        if form.is_valid():
            Name = form.data['name']
            CompanyName = form.data['company']
            #return HttpResponse(str(Company))
            """
            try:
                founder = Entity.objects.get(name=Name)
            except not Entity.DoesNotExist:
                return HttpResponse("He already exists, genius!")
                founder = Entity.objects.create(name=Name)
            """    
            if Entity.objects.filter(name=Name).count() > 0:
                founder = Entity.objects.get(name=Name)
            else:
                founder = Entity.objects.create(name=Name)
            
            try:
                company = Company.objects.get(name=CompanyName)
                founder.founding_company.add(company)
            except Company.DoesNotExist:
                return render(request, 'addFounderOne.html', {'form': form, 'error':'Please enter a company that exists.'})

            founder.save()
            return redirect("portfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = FounderForm() #A empty, unbound form
        return render(request, 'addFounderOne.html', {'form': form})
#add investor form, founder form(Check), and rounds form.

def addInvestorOne(request):
    if request.method == 'POST':
        form = InvestorForm(request.POST)
        if form.is_valid():
            return redirect("portfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = InvestorForm() #A empty, unbound form
        return render(request, 'addInvestorOne.html', {'form': form})

def addRoundOne(request):
    if request.method == 'POST':
        form = RoundForm(request.POST)
        if form.is_valid():
            return redirect("portfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = RoundForm() #A empty, unbound form
        return render(request, 'addRoundOne.html', {'form': form})

def addRightOne(request):
    if request.method == 'POST':
        form = RightForm(request.POST)
        if form.is_valid():
            return redirect("portfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = RightForm() #A empty, unbound form
        return render(request, 'addRightOne.html', {'form': form})

#add investor form(Check), founder form(Check), and rounds form(Check), and rights form(Check).