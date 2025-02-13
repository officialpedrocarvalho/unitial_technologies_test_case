"""
URL configuration for unitial_technologies project.

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
from django.urls import path

from data_analyzer import views

urlpatterns = [
    path('api/machine/', views.register_machines, name='register_machines'),
    path('api/machine/analysis/', views.machine_analysis, name='machine_analysis'),
    path('api/machine/highest_consumption_day/', views.highest_consumption_day, name='highest_consumption_day'),
]