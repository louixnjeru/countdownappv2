from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('search', views.search, name='search'),
    path('station/<str:id>', views.station, name='station'),
    #path('arrivals/<str:id>', views.arrivals, name='arrivals'),
    path('stop/<str:id>', views.stop, name='stop'),
    path('vehicle', views.vehicle, name='vehicle'),
    path('nearby', views.nearby, name='nearby'),
    ]

