from django.urls import path
from . import views

urlpatterns = [
   path('analysis/', views.analysis, name = 'analysis'),
   path('data_status/', views.data_status, name = 'data_status')
]
