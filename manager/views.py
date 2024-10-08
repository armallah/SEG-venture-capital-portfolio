from django.shortcuts import render , redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import Document, Company, Entity, Investing, Right, User, Round
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
                if user.user_type == 1:
                    return redirect('dashboard')
                elif user.user_type == 2:
                    return redirect('adminDashboard')
            else:
                messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")

    form = LoginForm()
    return render(request, 'login.html' , {'form':form})

def get_country_data():
    labels = []
    data = []
    allCountries = []
    queryset = Company.objects.all()
    for entry in queryset:
        allCountries.append(entry.country_code)
    labels = list(dict.fromkeys(allCountries))
    for country in labels:
        data.append(allCountries.count(country))
    return [labels, data]

def get_top_invest_data():
    labels = []
    data = []
    allCountries = []
    queryset = Company.objects.all().filter(wayra_investment__gt=0).order_by("-wayra_investment")[:5]
    for company in queryset:
        labels.append(company.name)
        data.append(round(int(company.wayra_investment), 0))
    return [labels, data]

def get_top_invest_rounds_data():
    labels = []
    data = []
    rounds = []
    companyNames = []
    topCompanies = Company.objects.all().filter(wayra_investment__gt=0).order_by("-wayra_investment")[:5]
    for company in topCompanies:
        compRounds = Round.objects.all().filter(company=company).order_by('round_number')
        entry = []
        for r in compRounds:
            entry.append(int(r.pre_money_valuation))
        rounds.append(entry)

    max = 0
    for i in range(len(rounds)):
        if len(rounds[i]) > max:
            max = len(rounds[i])

    for i in range(1, max + 1):
        labels.append("Round " + str(i))

    for i in range(0,5):
        try:
            companyNames.append(str(topCompanies[i].name))
            data.append(rounds[i])
        except:
            companyNames.append("")
            data.append([])

    return [labels, data, companyNames]

def get_dashboard_context():
    companies = Company.objects.all()
    entities = Entity.objects.all()
    moneyInvested = 0
    allFounders = []
    allInvestors = []
    portfolioCompanies = []

    for company in companies:
        moneyInvested += company.wayra_investment
        if company.wayra_investment > 0:
            portfolioCompanies.append(company)

    for entity in entities:
        if entity.getTotalFoundedCompanies() > 0:
            allFounders.append(entity)
        if entity.getTotalInvestedCompanies() > 0:
            allInvestors.append(entity)

    if moneyInvested >= 1000000000:
        investUnit = "b"
        moneyInvested = float(moneyInvested) / 1000000000
        moneyInvested = round(moneyInvested, 2)
    elif moneyInvested >= 1000000:
        investUnit = "m"
        moneyInvested = float(moneyInvested) / 1000000
        moneyInvested = round(moneyInvested, 2)
    else:
        investUnit = ""
        moneyInvested = round(moneyInvested, 0)
        moneyInvested = f"{moneyInvested:,}"

    doughnutChart = get_country_data()
    barChart = get_top_invest_data()
    lineChart = get_top_invest_rounds_data()

    context = {
        'totalInvestment' : moneyInvested,
        'totalCompanies' : len(portfolioCompanies),
        'totalInvestors' : len(allInvestors),
        'totalFounders' : len(allFounders),
        'investUnit' : investUnit,
        'doughnutLabels' : (doughnutChart[0]),
        'doughnutData' : (doughnutChart[1]),
        'barLabels' : (barChart[0]),
        'barData' : (barChart[1]),
        'lineLabels' : lineChart[0],
        'lineData1' : lineChart[1][0],
        'lineName1' : [lineChart[2][0]],
        'lineData2' : lineChart[1][1],
        'lineName2' : [lineChart[2][1]],
        'lineData3' : lineChart[1][2],
        'lineName3' : [lineChart[2][2]],
        'lineData4' : lineChart[1][3],
        'lineName4' : [lineChart[2][3]],
        'lineData5' : lineChart[1][4],
        'lineName5' : [lineChart[2][4]],
    }
    return context

@login_required(login_url="/login")
def dashboard(request):
    return render(request, 'dashboard.html', get_dashboard_context())

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def adminDashboard(request):
    return render(request, 'adminDashboard.html', get_dashboard_context())

from django.shortcuts import render, get_object_or_404
from .models import Entity, Company

@login_required(login_url="/login")
def entity_view(request, name):
    entity = get_object_or_404(Entity, name=name)

    return render(request, 'entity_details.html', {'entity': entity})

@login_required(login_url="/login")
def company_view(request, name):

    company = get_object_or_404(Company, name=name)

    return render(request, 'company_details.html', {'company': company})



def get_all_investors():
    data = Entity.objects.all()
    investingCompanies = []

    for entry in data:
        if (entry.getTotalInvestedCompanies() > 0):
            investingCompanies.append(entry)

    return investingCompanies

@login_required(login_url="/login")
def entities(request):
    context = {
        'data' : get_all_investors()
    }
    return render(request, 'entities.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def adminEntities(request):
    context = {
        'data' : get_all_investors()
    }
    return render(request, 'adminEntities.html', context)

@login_required(login_url="/login")
def sync(request):
    if request.method == 'POST':
        airtable.update_all()
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

def get_all_founders():
    data = Entity.objects.all()
    foundingCompanies = []

    for entry in data:
        if (entry.getTotalFoundedCompanies() > 0):
            foundingCompanies.append(entry)

    return foundingCompanies

@login_required(login_url="/login")
def founders(request):
    context = {
        'data' : get_all_founders()
    }
    return render(request, 'founders.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def adminFounders(request):
    context = {
        'data' : get_all_founders()
    }
    return render(request, 'adminFounders.html', context)

def error_404(request, exception):
    return render(request, '404.html')

def get_all_portfolio_companies():
    portfolioCompanies = Company.objects.filter(wayra_investment__gt=0) #.filter(wayra_investment!=0) #.order_by('date')
    return portfolioCompanies

@login_required(login_url="/login")
def portfolio(request):
    context = {
        'data' : get_all_portfolio_companies(),
    }
    return render(request, 'portfolio.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def deleteCompanyFounder(request, compID, founderID):
    comp = Company.objects.get(id=compID)
    founder = comp.founders.get(id=founderID)
    comp.founders.remove(founder)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def deleteCompanyInvestor(request, compID, investorID):
    comp = Company.objects.get(id=compID)
    investor = comp.investors.get(id=investorID)
    comp.investors.remove(investor)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def deleteCompanyRound(request, compID, roundID):
    comp = Company.objects.get(id=compID)
    round = comp.rounds.get(id=roundID)
    round.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def deleteCompanyRight(request, compID, rightID):
    comp = Company.objects.get(id=compID)
    right = comp.wayra_right.get(id=rightID)
    right.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/login")
def company_founders(request, company_name):
    company = get_object_or_404(Company, name=company_name)
    context = {'company': company, 'admin': admin_test(request.user)}

    return render(request, 'founders_details.html', context)

@login_required(login_url="/login")
def company_investors(request, company_name):
    company = get_object_or_404(Company, name=company_name)
    context = {'company': company, 'admin': admin_test(request.user)}

    return render(request, 'investors_details.html', context)

@login_required(login_url="/login")
def company_rounds(request, company_name):
    company = get_object_or_404(Company, name=company_name)
    context = {'company': company, 'admin': admin_test(request.user)}

    return render(request, 'rounds_details.html', context)

@login_required(login_url="/login")
def company_rights(request, company_name):
    company = get_object_or_404(Company, name=company_name)
    context = {'company': company, 'admin': admin_test(request.user)}

    return render(request, 'rights_details.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def adminPortfolio(request):
    context = {
        'data' : get_all_portfolio_companies(),
    }
    return render(request, 'adminPortfolio.html', context)

def get_all_ecosystem_companies():
    ecosystemCompanies = Company.objects.filter(wayra_investment=0) #.filter(wayra_investment==0) #.order_by('date')
    return ecosystemCompanies

@login_required(login_url="/login")
def ecosystem(request):
    context = {
        'data' : get_all_ecosystem_companies(),
    }
    return render(request, 'ecosystem.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def adminEcosystem(request):
    context = {
        'data' : get_all_ecosystem_companies(),
    }
    return render(request, 'adminEcosystem.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def users(request):
    allUsers = User.objects.all().filter(user_type=1)
    context = {
        'data' : allUsers,
    }
    return render(request, 'users.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def adminDeleteCompany(request, compID):
    comp = Company.objects.get(id=compID)
    comp.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def adminAddUser(request):
    if request.method == 'POST':
        form = AddNewUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New User added successfully.')
            form = AddNewUser()

    else:
        form = AddNewUser()
    context = {
        'form': form
    }
    return render(request, 'admin_add_user.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
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

    else:
        form = AddNewUser(initial={'first_name': account.first_name, 'last_name': account.last_name, 'email': account.email})
    context = {
        'form': form,
        'account': account,
    }

    return render(request, 'admin_edit_user.html', context)

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def adminDeleteUser(request, userID):
    account = User.objects.get(id=userID)
    account.delete()
    return HttpResponseRedirect(reverse('users'))

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def addCompany(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                df = pd.read_excel(request.FILES['upload'], dtype = {'Name':'string', 'Number':'string', 'Country':'string', 'Investors': 'string', 'Founders': 'string', 'Rights': 'string', 'Wayra Investment': 'float', 'Description': 'string'})
            except:
                return render(request, 'addCompany.html', {'form': form, 'error':'Please make sure your file is in the correct format.'})

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
                        investorName = investorList[i].strip()
                        try:
                            investorEntity = Entity.objects.get(name = investorName)
                            Investor = Investing.objects.create(investor = investorEntity, company = company, amount = float(investorList[i+1]))
                            Investor.save()
                            company.investors.add(investorEntity)
                        except Entity.DoesNotExist:
                            investorEntity = Entity.objects.create(name = investorName)
                            Investor = Investing.objects.create(investor = investorEntity, company = company, amount = float(investorList[i+1]))
                            investorEntity.save()
                            Investor.save()
                            company.investors.add(investorEntity)

                        company.investors.add(investorEntity)


                    founderList = df.iloc[x, 4].split(",")

                    for founderName in founderList:
                        try:
                            founder = Entity.objects.get(name = founderName.strip())
                            company.founders.add(founder)
                        except Entity.DoesNotExist:
                            founder = Entity.objects.create(name = founderName.strip())
                            company.founders.add(founder)
                        founder.save()

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
            return redirect("adminPortfolio")
        else:
            return render(request, 'addCompany.html', {'form': form, 'error':'Please upload a .xlsx file.'})
    else:
        form = DocumentForm()
        return render(request, 'addCompany.html', {'form': form})

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def addCompanyOne(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            Name = form.data['name'].strip()

            Number = form.data['number'].strip()
            if Company.objects.filter(number=Number).count() > 0:
                return render(request, 'addCompanyOne.html', {'form': form, 'error': 'There already exist a company with this Wayra number.'})
            Country = form.data['country_code'].strip()
            WayraInvestment = form.data['wayra_investment']
            Description = form.data['description'].strip()
            FounderName = form.data['founder_Name'].strip()
            try:
                founder = Entity.objects.get(name=FounderName)
            except Entity.DoesNotExist:
                founder = Entity.objects.create(name=FounderName)

            newCompany = Company.objects.create(name=Name, number=Number, country_code=Country, wayra_investment=WayraInvestment, description=Description)
            newCompany.founders.add(founder)

            newCompany.save()
            return redirect("adminPortfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = CompanyForm()
        return render(request, 'addCompanyOne.html', {'form': form})

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def addFounderOne(request):
    if request.method == 'POST':
        form = FounderForm(request.POST)

        if form.is_valid():
            Name = form.data['name'].strip()
            CompanyName = form.data['company'].strip()

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
            return redirect("adminPortfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = FounderForm()
        return render(request, 'addFounderOne.html', {'form': form})


@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def addInvestorOne(request):
    if request.method == 'POST':
        form = InvestorForm(request.POST)
        if form.is_valid():
            Name = form.data['name'].strip()
            CompanyName = form.data['company'].strip()
            Amount = form.data['amount']

            if Entity.objects.filter(name=Name).count() > 0:
                investorEntity = Entity.objects.get(name=Name)
            else:
                investorEntity = Entity.objects.create(name=Name)

            try:
                company = Company.objects.get(name=CompanyName)
                Investor = Investing.objects.create(investor = investorEntity, company = company, amount = Amount)
            except Company.DoesNotExist:
                return render(request, 'addInvestorOne.html', {'form': form, 'error':'Please enter a company that exists.'})

            return redirect("adminPortfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = InvestorForm()
        return render(request, 'addInvestorOne.html', {'form': form})

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def addRoundOne(request):
    if request.method == 'POST':
        form = RoundForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("adminPortfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = RoundForm()
        return render(request, 'addRoundOne.html', {'form': form})

@login_required(login_url="/login")
@user_passes_test(admin_test, login_url='adminProhibitted')
def addRightOne(request):
    if request.method == 'POST':
        form = RightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("adminPortfolio")
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = RightForm()
        return render(request, 'addRightOne.html', {'form': form})
