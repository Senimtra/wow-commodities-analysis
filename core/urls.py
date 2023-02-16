from django.urls import path
from . import views

urlpatterns = [
   path('analysis/', views.analysis, name = 'analysis')
]
