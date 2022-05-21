from django.contrib.auth import logout, login, authenticate
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from .config import auth_token
from .models import *
import http.client
import json
from .forms import RegistrationForm
from .forms import UserSignInForm
from django.contrib import messages
from .forms import AddNewsForm


def index(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/BSA/matches?status=LIVE', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    live_games = []

    for match in response['matches']:
        live_games.append({
            'home_team': match['homeTeam']['name'],
            'away_team': match['awayTeam']['name'],
            'home_team_score': match['score']['fullTime']['homeTeam'],
            'away_team_score': match['score']['fullTime']['awayTeam']
        })

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/BSA/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    teams = []
    count = 0

    for team in response['standings'][0]['table']:
        teams.append({
            'position': team['position'],
            'name': team['team']['name'],
            'played_games': team['playedGames'],
            'goal_difference': team['goalDifference'],
            'points': team['points']
        })

        count = count + 1

        if count == 10:
            break

    latest_news = News.objects.order_by('-date_time')

    if len(latest_news) > 5:
        latest_news = latest_news[:5]

    context = {
        'live_games': live_games,
        'teams': teams,
        'latest_news': latest_news
    }

    return render(request, 'golden_goal/index.html', context)


def results(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/BSA/matches?status=FINISHED', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    matches = response['matches']

    def my_func(val):
        return val['matchday']

    matches.sort(key=my_func)
    matchdays = []
    curr_matchday = 0

    for match in matches:
        game = {
            'home_team': match['homeTeam']['name'],
            'home_team_crest': 'images/team_' + str(match['homeTeam']['id']) + ".png",
            'home_team_score': match['score']['fullTime']['homeTeam'],
            'away_team': match['awayTeam']['name'],
            'away_team_crest': 'images/team_' + str(match['awayTeam']['id']) + ".png",
            'away_team_score': match['score']['fullTime']['awayTeam']
        }

        if match['matchday'] > curr_matchday:
            matchday = {
                'matchday': match['matchday'],
                'games': [game]
            }

            matchdays.append(matchday)
            curr_matchday = match['matchday']
        else:
            matchdays[match['matchday'] - 1]['games'].append(game)

    matchdays = matchdays[::-1]

    for i in range(len(matchdays)):
        matchdays[i]['id'] = i

    context = {
        'matchdays': matchdays
    }

    return render(request, 'golden_goal/results.html', context)


def prediction(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/BSA/matches?status=LIVE', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    matches = response['matches']

    def my_func(val):
        return val['matchday']

    matches.sort(key=my_func)
    live_matchdays = []

    for i in range(38):
        live_matchdays.append({
            'matchday': i + 1,
            'games': []
        })

    for match in matches:
        live_matchdays[match['matchday'] - 1]['games'].append({
            'home_team': match['homeTeam']['name'],
            'home_team_crest': 'images/team_' + str(match['homeTeam']['id']) + ".png",
            'home_team_score': match['score']['fullTime']['homeTeam'],
            'away_team': match['awayTeam']['name'],
            'away_team_crest': 'images/team_' + str(match['awayTeam']['id']) + ".png",
            'away_team_score': match['score']['fullTime']['awayTeam']
        })

    live_matchdays = [matchday for matchday in live_matchdays if len(matchday['games']) != 0]

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/BSA/matches', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    matches = response['matches']
    matches.sort(key=my_func)
    scheduled_matchdays = []

    for i in range(38):
        scheduled_matchdays.append({
            'matchday': i + 1,
            'games': []
        })

    for match in matches:
        if match['status'] != "SCHEDULED":
            continue

        scheduled_matchdays[match['matchday'] - 1]['games'].append({
            'home_team': match['homeTeam']['name'],
            'home_team_crest': 'images/team_' + str(match['homeTeam']['id']) + ".png",
            'away_team': match['awayTeam']['name'],
            'away_team_crest': 'images/team_' + str(match['awayTeam']['id']) + ".png",
            'datetime': match['utcDate'][:10] + " " + match['utcDate'][11:16] + "h"
        })

    scheduled_matchdays = [matchday for matchday in scheduled_matchdays if len(matchday['games']) != 0]

    for i in range(len(scheduled_matchdays)):
        scheduled_matchdays[i]['id'] = i

    context = {
        'live_matchdays': live_matchdays,
        'scheduled_matchdays': scheduled_matchdays
    }

    return render(request, 'golden_goal/prediction.html', context)


def standings(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/BSA/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    teams = []

    for team in response['standings'][0]['table']:
        teams.append({
            'position': team['position'],
            'crest': 'images/team_' + str(team['team']['id']) + ".png",
            'name': team['team']['name'],
            'played_games': team['playedGames'],
            'won': team['won'],
            'draw': team['draw'],
            'lost': team['lost'],
            'goals_for': team['goalsFor'],
            'goals_against': team['goalsAgainst'],
            'goal_difference': team['goalDifference'],
            'points': team['points']
        })

    context = {
        'teams': teams
    }

    return render(request, 'golden_goal/standings.html', context)


def scorers(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/BSA/scorers', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    players = []
    count = 1

    for player in response['scorers']:
        players.append({
            'rank': count,
            'name': player['player']['name'],
            'team': player['team']['name'],
            'position': player['player']['position'],
            'number_of_goals': player['numberOfGoals']
        })

        count = count + 1

    context = {
        'players': players
    }

    return render(request, 'golden_goal/scorers.html', context)


def user_rang_list(request: HttpRequest):
    users = User.objects.order_by('score')
    users = [user for user in users if user.type != 'administrator' and user.type != 'moderator']

    ranked_users = []
    rank = 1

    for user in users:
        ranked_users.append({
            'username': user.username,
            'rank': rank,
            'score': user.score
        })

        rank += 1

    context = {
        'ranked_users': ranked_users
    }

    return render(request, 'golden_goal/user_rang_list.html', context)


def log_out(request: HttpRequest):
    logout(request)
    return redirect('home')


def user_profile(request: HttpRequest):
    users = User.objects.order_by('score')
    rank = 1

    for user in users:
        if request.user.username == user.username:
            break
        else:
            rank += 1

    context = {
        'rank': rank
    }

    return render(request, 'golden_goal/user_profile.html', context)


def user_images(request: HttpRequest):
    users = User.objects.order_by('score')
    rank = 1

    for user in users:
        if request.user.username == user.username:
            break
        else:
            rank += 1

    context = {
        'rank': rank
    }

    return render(request, 'golden_goal/user_images.html', context)


def user_administration(request: HttpRequest):
    users = User.objects.filter(type='user')
    moderators = User.objects.filter(type='moderator')

    context = {
        'users': users,
        'moderators': moderators
    }

    return render(request, 'golden_goal/user_administration.html', context)


def sign_up(request: HttpRequest):
    registration_form = RegistrationForm(data=request.POST or None)

    if registration_form.is_valid():
        user = registration_form.save(commit=False)
        user.type = 'user'
        user.save()
        login(request, user)
        messages.info(request, 'Successful registration')
        return redirect('sign_up')

    context = {
        'registration_form': registration_form
    }

    return render(request, 'golden_goal/sign_up.html', context)


def sign_in(request: HttpRequest):
    sign_in_form = UserSignInForm(data=request.POST or None)

    if sign_in_form.is_valid():
        username = sign_in_form.cleaned_data["username"]
        password = sign_in_form.cleaned_data["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    context = {
        'sign_in_form': sign_in_form,
    }

    return render(request, 'golden_goal/sign_in.html', context)


def add_news(request: HttpRequest):
    news_form = AddNewsForm(request.POST or None)

    if news_form.is_valid():
        vest = news_form.save(commit=False)
        vest.author = User.objects.get(username=request.user.get_username())
        vest.save()
        return redirect('home')

    context = {
        'news_form': news_form
    }

    return render(request, 'golden_goal/add_news.html', context)


def news(request: HttpRequest, news_id):
    try:
        curr_news = News.objects.get(pk=news_id)
        author = User.objects.get(pk=curr_news.author.id)
        comments = Comment.objects.filter(news_id=news_id)

        context = {
            'news': curr_news,
            'author': author,
            'comments': comments
        }

        return render(request, 'golden_goal/news.html', context)
    except News.DoesNotExist:
        raise Http404("News not found!")
