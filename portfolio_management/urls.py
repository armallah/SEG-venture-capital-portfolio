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
    path('companies/<str:company_name>/founders/', views.company_founders, name='company_founders'),
    path('companies/<str:company_name>/investors/', views.company_investors, name='company_investors'),
    path('entities/', views.entities, name = 'entities'),
    path('founders/', views.founders, name = 'founders'),
    path('ecosystem/', views.ecosystem, name = 'ecosystem'),
    path('users/', views.users, name = 'users'),
    path('adminAddUser/', views.adminAddUser, name='adminAddUser'),
    path('adminDeleteUser/<int:userID>', views.adminDeleteUser, name='adminDeleteUser'),
    path('adminEditUser/<int:userID>', views.adminEditUser, name='adminEditUser'),
    path('add/company', views.addCompany, name = 'add_company'),
    path('add/companyOne', views.addCompanyOne, name = 'add_company_one'),
    path('adminProhibitted/', views.adminProhibitted, name='adminProhibitted'),
]


handler404 = views.error_404
