from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name = 'home'),
   path('analysis/', views.analysis, name = 'analysis'),
   path('data_status/', views.data_status, name = 'data_status')
]
