# habits/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complete_habit/<int:habit_id>/', views.complete_habit, name='complete_habit'),
]

