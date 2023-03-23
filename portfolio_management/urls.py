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

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home , name="home"),
    path('sync/', views.sync, name="sync airtable"),
    path("login/" , views.log_in , name="log_in"),
    path('log_out/', views.log_out, name = 'log_out'),
    path('entities/<str:name>/', views.entity_view, name='entity_view'),
    path('companies/<str:name>/', views.company_view, name='company_view'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('portfolio/', views.portfolio, name = 'portfolio'),
    path('entities/', views.entities, name = 'entities'),
    path('founders/', views.founders, name = 'founders'),
    path('ecosystem/', views.ecosystem, name = 'ecosystem'),
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
]


handler404 = views.error_404
