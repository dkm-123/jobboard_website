"""
URL configuration for jobboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from job import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('user_home/',views.user_home, name="user_home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('Logout/', views.Logout, name="Logout"),
    path('recruiter_home/', views.recruiter_home, name='recruiter_home'),
    path("admin_home/", views.admin_home, name="admin_home"),
    path('view-users/', views.view_users, name='view_users'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
    path('recruiters_pending/', views.recruiters_pending, name='recruiters_pending'),
    path('accepted_recruiters/', views.accepted_recruiters, name='accepted_recruiters'),
    path('rejected_recruiters/', views.rejected_recruiters, name='rejected_recruiters'),
    path('all_recruiters/', views.all_recruiters, name='all_recruiters'),
    path('accept_recruiter/<int:id>/', views.accept_recruiter, name='accept_recruiter'),
    path('reject_recruiter/<int:id>/', views.reject_recruiter, name='reject_recruiter'),
    path('accepted_recruiters/', views.accepted_recruiters, name='accepted_recruiters'),
    path('rejected_recruiters/', views.rejected_recruiters, name='rejected_recruiters'),
    path('all_recruiters/', views.all_recruiters, name='all_recruiters'),
    path('changepassword_admin/', views.changepassword_admin, name='changepassword_admin'),
    path('changepassword_jobseeker/', views.changepassword_jobseeker, name='changepassword_jobseeker'),
]

