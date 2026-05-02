"""
URL configuration for ClassroomSync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from Booking import views

urlpatterns = [
    path('', views.home, name="home"),
    path('Admin-Login/', views.admin_login, name="admin_login"),
    path('Student-Faculty-Dashboard/', views.student_dashboard, name="student_dashboard"),
    path('Admin-Dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('add-alert/', views.add_alert, name='add_alert'),
    path('delete-alert/<int:id>/', views.delete_alert, name='delete_alert'),
    path('Classroom-Details/<str:room_number>/', views.classroom_details, name="classroom_details"),
    path('logout/', views.logout_view, name='logout_view')
]