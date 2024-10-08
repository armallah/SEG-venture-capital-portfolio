"""portfolio_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from manager import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home , name="home"),
    path('sync/', views.sync, name="sync airtable"),
    path("login/" , views.log_in , name="log_in"),
    path('log_out/', views.log_out, name = 'log_out'),
    path('entities/<str:name>/', views.entity_view, name='entity_view'),
    path('companies/<str:name>/', views.company_view, name='company_view'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('adminDashboard/', views.adminDashboard, name = 'adminDashboard'),
    path('portfolio/', views.portfolio, name = 'portfolio'),
    path('adminPortfolio/', views.adminPortfolio, name = 'adminPortfolio'),
    path('entities/', views.entities, name = 'entities'),
    path('adminEntities/', views.adminEntities, name = 'adminEntities'),
    path('founders/', views.founders, name = 'founders'),
    path('adminFounders/', views.adminFounders, name = 'adminFounders'),
    path('ecosystem/', views.ecosystem, name = 'ecosystem'),
    path('adminEcosystem/', views.adminEcosystem, name = 'adminEcosystem'),
    path('users/', views.users, name = 'users'),
    path('adminAddUser/', views.adminAddUser, name='adminAddUser'),
    path('adminDeleteUser/<int:userID>', views.adminDeleteUser, name='adminDeleteUser'),
    path('adminDeleteCompany/<int:compID>', views.adminDeleteCompany, name='adminDeleteCompany'),
    path('adminEditUser/<int:userID>', views.adminEditUser, name='adminEditUser'),
    path('add/companySpreadsheet', views.addCompany, name = 'add_company'),
    path('add/company', views.addCompanyOne, name = 'add_company_one'),
    path('add/founder',views.addFounderOne, name = 'add_founder_one'),
    path('add/investor',views.addInvestorOne, name = 'add_investor_one'),
    path('add/right',views.addRightOne, name = 'add_right_one'),
    path('add/round',views.addRoundOne, name = 'add_round_one'),
    path('adminProhibitted/', views.adminProhibitted, name='adminProhibitted'),
    path('companies/<str:company_name>/founders/', views.company_founders, name='company_founders'),
    path('companies/<str:company_name>/investors/', views.company_investors, name='company_investors'),


    path('companies/<str:company_name>/rounds/', views.company_rounds, name='company_rounds'),
    path('companies/<str:company_name>/rights/', views.company_rights, name='company_rights'),

    path('deleteCompanyFounder/<int:compID>/<int:founderID>', views.deleteCompanyFounder, name='deleteCompanyFounder'),
    path('deleteCompanyInvestor/<int:compID>/<int:investorID>', views.deleteCompanyInvestor, name='deleteCompanyInvestor'),
    path('deleteCompanyRound/<int:compID>/<int:roundID>', views.deleteCompanyRound, name='deleteCompanyRound'),
    path('deleteCompanyRight/<int:compID>/<int:rightID>', views.deleteCompanyRight, name='deleteCompanyRight'),

    path('reset_password' , auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/' , auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html") , name= "password_reset_complete")
]


handler404 = views.error_404
