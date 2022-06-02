# autori:
# Dejan Kovacevic 0167/2019
# Srdjan Kuzmanovic 0169/2019
# Kosta Mladenovic 0283/2019
# Joze Vodnik 0125/2019
# definisanje ruta aplikacije

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
    path('delete_moderator', delete_moderator, name='delete_moderator'),
    path('live_games_index', live_games_index, name='live_games_index'),
    path('update_news/<int:news_id>', update_news, name='update_news'),
    path('comment_news/<int:news_id>', comment_news, name='comment_news'),
    path('reply_comment/<int:comment_id>', reply_comment, name='reply_comment'),
    path('delete_news', delete_news, name='delete_news'),
    path('delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),
    path('prediction/predict_match/', predict_match, name='predict_match'),
    path('live_results', live_results, name='live_results'),
    path('take_presents', take_presents, name='take_presents'),
    path('double_prediction_count', double_prediction_count, name='double_prediction_count'),
    path('change_profile_image', change_profile_image, name='change_profile_image')
]
