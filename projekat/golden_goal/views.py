from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from .config import auth_token
from .models import *
import http.client
import json


def index(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/PL/matches?status=LIVE', None, headers)
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
    connection.request('GET', '/v2/competitions/PL/standings', None, headers)
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

    context = {
        'live_games': live_games,
        'teams': teams
    }

    return render(request, 'golden_goal/index.html', context)


def results(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/PL/matches?status=FINISHED', None, headers)
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
            'away_team': match['awayTeam']['name'],
            'home_team_score': match['score']['fullTime']['homeTeam'],
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

    context = {
        'matchdays': matchdays
    }

    return render(request, 'golden_goal/results.html', context)


def prediction(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/PL/matches?status=LIVE', None, headers)
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
            'away_team': match['awayTeam']['name'],
            'home_team_score': match['score']['fullTime']['homeTeam'],
            'away_team_score': match['score']['fullTime']['awayTeam']
        })

    live_matchdays = [matchday for matchday in live_matchdays if len(matchday['games']) != 0]

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/PL/matches', None, headers)
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
            'away_team': match['awayTeam']['name'],
            'datetime': match['utcDate'][:10] + " " + match['utcDate'][11:16] + "h"
        })

    scheduled_matchdays = [matchday for matchday in scheduled_matchdays if len(matchday['games']) != 0]

    context = {
        'live_matchdays': live_matchdays,
        'scheduled_matchdays': scheduled_matchdays
    }

    return render(request, 'golden_goal/prediction.html', context)


def standings(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token}
    connection.request('GET', '/v2/competitions/PL/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    teams = []

    for team in response['standings'][0]['table']:
        teams.append({
            'position': team['position'],
            'crest': team['team']['crestUrl'],
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
    connection.request('GET', '/v2/competitions/PL/scorers', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    players = []
    count = 1

    for player in response['scorers']:
        players.append({
            'rank': count,
            'name': player['player']['name'],
            'team': player['team']['name'],
            'position': player['player']['name'],
            'number_of_goals': player['numberOfGoals']
        })

        count = count + 1

    context = {
        'players': players
    }

    return render(request, 'golden_goal/scorers.html', context)


def user_rang_list(request: HttpRequest):
    return render(request, 'golden_goal/user_rang_list.html')


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
