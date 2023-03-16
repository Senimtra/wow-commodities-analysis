from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name = 'home'),
   path('analysis/', views.analysis, name = 'analysis'),
   path('market/', views.market, name = 'market'),
   path('distribution/', views.distribution, name = 'distribution'),
   path('profit/', views.profit, name = 'profit'),
   path('profit/details/<int:item_id>', views.details, name = 'details'),
   path('data/', views.data, name = 'data')
]
