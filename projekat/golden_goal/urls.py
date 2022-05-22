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
    path('user_profile/', user_profile, name='user_profile'),
    path('user_images/', user_images, name='user_images'),
    path('user_administration/', user_administration, name='user_administration'),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('add_news/', add_news, name='add_news'),
    path('news/<int:news_id>', news, name='news'),
    path('search_news', search_news, name='search_news'),
    path('make_moderator', make_moderator, name='make_moderator'),
    path('delete_user', delete_user, name='delete_user'),
    path('unmake_moderator', unmake_moderator, name='unmake_moderator'),
    path('delete_moderator', delete_moderator, name='delete_moderator')
]
