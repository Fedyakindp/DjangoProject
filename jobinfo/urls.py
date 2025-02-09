from django.urls import path
from . import views

urlpatterns = [
    path('jobinfo/', views.hello, name='hello'),
    path('stat/', views.stat, name='stat'),
    path('demand/', views.demand, name='demand'),
    path('geo/', views.geo, name='geo'),
    path('skills/', views.skills, name='skills'),
    path('vacancies/', views.vacancies, name='vacancies'),
]