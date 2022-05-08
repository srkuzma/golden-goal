from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('results/', results, name='results'),
    path('prediction/', prediction, name='prediction'),
    path('standings/', standings, name='standings'),
    path('scorers/', scorers, name='scorers'),
    path('user_rang_list/', user_rang_list, name='user_rang_list'),
    path('log_out/', log_out, name='log_out'),
    path('user_profile/', user_profile, name='user_profile')
]
