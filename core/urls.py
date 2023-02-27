from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name = 'home'),
   path('market/', views.market, name = 'market'),
   path('distribution/', views.distribution, name = 'distribution'),
   path('profit/', views.profit, name = 'profit'),
   path('data/', views.data, name = 'data')
]
