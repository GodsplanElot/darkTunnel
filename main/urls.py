from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('terms/', views.terms_of_use, name='terms_of_use'),
    path('Idusername/', views.Idusername, name='Idusername'),
    path('idpassword/', views.idpassword, name='idpassword'),
    
]