from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('results/', results, name='results'),
    path('prediction/', prediction, name='prediction'),
    path('standings/', standings, name='standings'),
    path('scorers/', scorers, name='scorers'),
    path('user_rang_list/', user_rang_list, name='user_rang_list')
]
