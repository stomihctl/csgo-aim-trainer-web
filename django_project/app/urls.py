"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', login, name='login'),
    path('entry_test/', entry_test, name='entry_test'),
    path('account_remove/', account_remove, name='account_remove'),
    path('attributes_input/', attributes_input, name='attributes_input'),
    path('request_training_plan/', request_training_plan, name='request_training_plan'),
    path('reset_password/', reset_password, name='reset_password'),
    path('single_training_request/', single_training_request, name='single_training_request'),
    path('trainer_selection/', trainer_selection, name='trainer_selection'),
    path('training_plan_generation/', training_plan_generation, name='training_plan_generation'),
    path('training_statistics/', training_statistics, name='training_statistics'),
    path('logoff/', logoff, name='logoff'),
    path('home/', home, name='home'),
    path('update_trainer_profile/', update_trainer_profile, name='update_trainer_profile'),
    path('choose_trainer/<int:trainer_id>/', choose_trainer, name='choose_trainer'),
    path('account_removal_request/', account_removal_request, name='account_removal_request'),
    path('remove_chosen_trainer/', remove_chosen_trainer, name='remove_chosen_trainer'),
    path('request_training_plan/<int:player_id>/', request_training_plan_for_player, name='request_training_plan_for_player'),
]
