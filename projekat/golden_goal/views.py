# autori:
# Dejan Kovacevic 0167/2019
# Srdjan Kuzmanovic 0169/2019
# Kosta Mladenovic 0283/2019
# Joze Vodnik 0125/2019

from random import randint
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.db.models import Q
from .config import *
import http.client
import json
from .forms import *
import pytz


# Funkcija za ucitavanje vesti, utakmica uzivo i sazete tabele timova na glavnu stranicu
# i dodavanje ili oduzimanje bodova korisnicima za predikcije za zavrsene meceve
# param request HttpRequest
# return HttpResponse
def index(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token2}
    connection.request('GET', '/v2/competitions/BSA/matches?status=LIVE', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    live_games = []

    for match in response['matches']:
        live_games.append({
            'home_team': match['homeTeam']['name'],
            'away_team': match['awayTeam']['name'],
            'home_team_score': match['score']['fullTime']['homeTeam'],
            'away_team_score': match['score']['fullTime']['awayTeam'],
        })

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token3}
    connection.request('GET', '/v2/competitions/BSA/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    teams = []
    count = 0

    for team in response['standings'][0]['table']:
        teams.append({
            'position': team['position'],
            'crest': 'images/team_' + str(team['team']['id']) + ".png",
            'name': team['team']['name'],
            'played_games': team['playedGames'],
            'goal_difference': team['goalDifference'],
            'points': team['points']
        })

        count = count + 1

        if count == 10:
            break

    latest_news = News.objects.order_by('-date_time')

    if len(latest_news) > 3:
        latest_news = latest_news[:3]

    context = {
        'live_games': live_games,
        'teams': teams,
        'latest_news': latest_news
    }

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token4}
    connection.request('GET', '/v2/competitions/BSA/matches?status=FINISHED', None, headers)
    response = json.loads(connection.getresponse().read().decode())

    def get_result(home_score, away_score):
        if home_score > away_score:
            return '1'
        elif home_score < away_score:
            return '2'
        else:
            return 'X'

    for match in response['matches']:
        match_id = match['id']
        home_team_score = match['score']['fullTime']['homeTeam']
        away_team_score = match['score']['fullTime']['awayTeam']
        predictions = Prediction.objects.filter(game=match_id)

        if predictions:
            for curr_prediction in predictions:
                curr_type = curr_prediction.type
                user = curr_prediction.user
                result = get_result(home_team_score, away_team_score)
                prediction_list = list(curr_type)

                if result in prediction_list:
                    user.score += 50
                else:
                    user.score -= 50

                user.save()
                curr_prediction.delete()

    return render(request, 'golden_goal/index.html', context)


# Funkcija koja se koristi u ajax pozivu u index.js kako bi se periodicno na svakih 10 s
# dobile utakmice uzivo i azurirao rezultat bez osvezavanja glavne stranice
# param request HttpRequest
# return JsonResponse
def live_games_index(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token1}
    connection.request('GET', '/v2/competitions/BSA/matches?status=LIVE', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    live_games = []

    for match in response['matches']:
        live_games.append({
            'home_team': match['homeTeam']['name'],
            'away_team': match['awayTeam']['name'],
            'home_team_score': match['score']['fullTime']['homeTeam'],
            'away_team_score': match['score']['fullTime']['awayTeam'],
        })

    return JsonResponse(json.dumps(live_games), safe=False)


# Funkcija za ucitavanje rezultata odigranih utakmica na results.html stranici
# param request HttpRequest
# return HttpResponse
def results(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token1}
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
            'home_team_crest': 'images/teams/team_' + str(match['homeTeam']['id']) + ".png",
            'home_team_score': match['score']['fullTime']['homeTeam'],
            'home_team_score_halftime': match['score']['halfTime']['homeTeam'],
            'away_team': match['awayTeam']['name'],
            'away_team_crest': 'images/teams/team_' + str(match['awayTeam']['id']) + ".png",
            'away_team_score': match['score']['fullTime']['awayTeam'],
            'away_team_score_halftime': match['score']['halfTime']['awayTeam']
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


# Funkcija koja se koristi u ajax pozivu u prediction.js kako bi se periodicno na svakih 10 s
# dobile utakmice uzivo i azurirao rezultat bez osvezavanja stranice prediction.html
# param request HttpRequest
# return JsonResponse
def live_results(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token2}
    connection.request('GET', '/v2/competitions/BSA/matches?status=LIVE', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    matches = response['matches']

    def my_func(val):
        return val['matchday']

    def get_prediction(match_id):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.get_username())
            predictions = Prediction.objects.filter(user=user, game=match_id)
            return predictions[0].type if len(predictions) > 0 else ''
        else:
            return ''

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
            'home_team_crest': 'images/teams/team_' + str(match['homeTeam']['id']) + ".png",
            'home_team_score': match['score']['fullTime']['homeTeam'],
            'away_team': match['awayTeam']['name'],
            'away_team_crest': 'images/teams/team_' + str(match['awayTeam']['id']) + ".png",
            'away_team_score': match['score']['fullTime']['awayTeam'],
            'id': match['id'],
            'prediction': get_prediction(match['id'])
        })

    live_matchdays = [matchday for matchday in live_matchdays if len(matchday['games']) != 0]
    return JsonResponse(json.dumps(live_matchdays), safe=False)


# Funkcija za ucitavanje utakmica uzivo i rasporeda utakmica na prediction.html stranicu
# param request HttpRequest
# return HttpResponse
def prediction(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token2}
    connection.request('GET', '/v2/competitions/BSA/matches?status=LIVE', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    matches = response['matches']

    def my_func(val):
        return val['matchday']

    def get_prediction(match_id):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.get_username())
            predictions = Prediction.objects.filter(user=user, game=match_id)
            return predictions[0].type if len(predictions) > 0 else ''
        else:
            return ''

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
            'home_team_crest': 'images/teams/team_' + str(match['homeTeam']['id']) + ".png",
            'home_team_score': match['score']['fullTime']['homeTeam'],
            'away_team': match['awayTeam']['name'],
            'away_team_crest': 'images/teams/team_' + str(match['awayTeam']['id']) + ".png",
            'away_team_score': match['score']['fullTime']['awayTeam']
        })

    live_matchdays = [matchday for matchday in live_matchdays if len(matchday['games']) != 0]

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token3}
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
            'home_team_crest': 'images/teams/team_' + str(match['homeTeam']['id']) + ".png",
            'away_team': match['awayTeam']['name'],
            'away_team_crest': 'images/teams/team_' + str(match['awayTeam']['id']) + ".png",
            'datetime': match['utcDate'][:10] + " " + match['utcDate'][11:16] + "h",
            'id': match['id'],
            'prediction': get_prediction(match['id'])
        })

    scheduled_matchdays = [matchday for matchday in scheduled_matchdays if len(matchday['games']) != 0]

    for i in range(len(scheduled_matchdays)):
        scheduled_matchdays[i]['id'] = i

    context = {
        'live_matchdays': live_matchdays,
        'scheduled_matchdays': scheduled_matchdays
    }

    return render(request, 'golden_goal/prediction.html', context)


# Funkcija koja ucitava stanje na tabeli prvenstva na standings.html
# param request HttpRequest
# return HttpResponse
def standings(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token4}
    connection.request('GET', '/v2/competitions/BSA/standings', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    teams = []

    for team in response['standings'][0]['table']:
        teams.append({
            'position': team['position'],
            'crest': 'images/teams/team_' + str(team['team']['id']) + ".png",
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


# Funkcija koja ucitava 10 najboljih strelaca prvenstva na scorers.html
# param request HttpRequest
# return HttpResponse
def scorers(request: HttpRequest):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': auth_token4}
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


# Funkcija koja ucitava rang listu registrovanih korisnika po broju poena na user_rang_list.html
# param request HttpRequest
# return HttpResponse
def user_rang_list(request: HttpRequest):
    users = User.objects.order_by('-score')
    users = [user for user in users if user.type != 'administrator' and user.type != 'moderator']

    ranked_users = []
    rank = 1

    for user in users:
        ranked_users.append({
            'username': user.username,
            'rank': rank,
            'score': user.score,
            'image': user.image
        })

        rank += 1

    context = {
        'ranked_users': ranked_users
    }

    return render(request, 'golden_goal/user_rang_list.html', context)


# Funkcija za odjavljivanje ulogovanog korisnika
# param request HttpRequest
# return HttpResponseRedirect
@login_required(login_url='sign_in')
def log_out(request: HttpRequest):
    logout(request)
    return redirect('home')


# Funkcija koja ucitava podatke o korisniku (rang, broj poena, tip i neotvorene poklone) na user_profile.html
# param request HttpRequest
# return HttpResponse
@login_required(login_url='sign_in')
def user_profile(request: HttpRequest):
    users = User.objects.order_by('-score')
    users = [user for user in users if user.type != 'administrator' and user.type != 'moderator']
    user = User.objects.get(username=request.user.get_username())

    if user.type == 'user':
        rank = users.index(user) + 1
    else:
        rank = -1

    presents = Present.objects.filter(user=user) if user.type == 'user' else []

    context = {
        'rank': rank,
        'presents': presents
    }

    return render(request, 'golden_goal/user_profile.html', context)


# Funkcija koja ucitava podatke o korisniku i  slike trenutno ulogovanog korisnika na user_images.html
# param request HttpRequest
# return HttpResponse
@login_required(login_url='sign_in')
def user_images(request: HttpRequest):
    user = User.objects.get(username=request.user.get_username())
    users = User.objects.order_by('-score')
    users = [user for user in users if user.type != 'administrator' and user.type != 'moderator']

    if user.type == 'user':
        rank = users.index(user) + 1
    else:
        rank = -1

    user_image_id = int(user.image[13:-4])
    images = UserImage.objects.filter(user=user).filter(~Q(image=user_image_id))

    context = {
        'rank': rank,
        'images': images
    }

    return render(request, 'golden_goal/user_images.html', context)


# Funkcija koja ucitava listu obicnih korisnika i moderatora na user_administration.html
# param request HttpRequest
# return HttpResponse
@login_required(login_url='sign_in')
def user_administration(request: HttpRequest):
    user = User.objects.get(username=request.user.get_username())

    if user.type == 'administrator':
        users = User.objects.filter(type='user')
        moderators = User.objects.filter(type='moderator')

        context = {
            'users': users,
            'moderators': moderators
        }

        return render(request, 'golden_goal/user_administration.html', context)
    else:
        return HttpResponse(status=403)


# Funkcija za registraciju novog korisnika koja koristi korisnicko ime i sifru
# param request HttpRequest
# return HttpResponse, HttpResponseRedirect
def sign_up(request: HttpRequest):
    registration_form = RegistrationForm(data=request.POST or None)

    if registration_form.is_valid():
        user = registration_form.save(commit=False)
        user.type = 'user'
        user.save()
        group_user = Group.objects.get(name='user')
        user.groups.add(group_user)
        user_image = UserImage(user=user, image=0)
        user_image.save()
        login(request, user)
        return redirect('home')

    context = {
        'registration_form': registration_form
    }

    return render(request, 'golden_goal/sign_up.html', context)


# Funkcija za logovanje registrovanog korisnika koja koristi korisnicko ime i lozinku
# Takodje,funkcija sluzi i za dodeljivanje nasumicno izabranog poklona korisniku ukoliko
# mu je ovo prvo logovanje u toku dana
# param request HttpRequest
# return HttpResponse, HttpResponseRedirect
def sign_in(request: HttpRequest):
    sign_in_form = UserSignInForm(data=request.POST or None)

    if request.user.is_authenticated:
        return HttpResponse(status=404)

    if sign_in_form.is_valid():
        username = sign_in_form.cleaned_data['username']
        password = sign_in_form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            last_login = user.last_login.date()
            current_date = datetime.datetime.now(pytz.timezone('UTC')).date()

            if user.type == 'user' and last_login != current_date:
                users = User.objects.order_by('-score')
                users = [user for user in users if user.type != 'administrator' and user.type != 'moderator']
                position = users.index(user) + 1

                if position > 20:
                    present_type = 'points'
                    points = randint(1, 5) * 50
                    present = Present(type=present_type, points=points, user=user)
                elif 10 < position <= 20:
                    present_type = 'points' if randint(0, 1) == 0 else 'image'

                    if present_type == 'points':
                        points = randint(1, 5) * 100
                        present = Present(type=present_type, points=points, user=user)
                    else:
                        image = randint(1, 30)
                        present = Present(type=present_type, image=image, user=user)
                else:
                    r = randint(0, 2)
                    present_type = 'points' if r == 0 else 'image' if r == 1 else 'double_prediction'

                    if present_type == 'points':
                        points = randint(1, 5) * 200
                        present = Present(type=present_type, points=points, user=user)
                    elif present_type == 'image':
                        image = randint(21, 41)
                        present = Present(type=present_type, image=image, user=user)
                    else:
                        present = Present(type=present_type, user=user)

                present.save()
                user.presents = user.presents + 1
                user.save()

            login(request, user)
            return redirect('home')

    context = {
        'sign_in_form': sign_in_form,
    }

    return render(request, 'golden_goal/sign_in.html', context)


# Funkcija za dodavanje nove vesti u aplikaciju (unosi se naslov, sazetak i sadrzaj vesti)
# param request HttpRequest
# return HttpResponse, HttpResponseRedirect
@login_required(login_url='sign_in')
@permission_required('golden_goal.add_news', raise_exception=True)
def add_news(request: HttpRequest):
    news_form = AddNewsForm(request.POST or None)

    if news_form.is_valid():
        curr_news = news_form.save(commit=False)
        curr_news.author = User.objects.get(username=request.user.get_username())
        curr_news.date_time = datetime.datetime.now()
        curr_news.save()
        return redirect('home')

    context = {
        'news_form': news_form
    }

    return render(request, 'golden_goal/add_news.html', context)


# Funkcija koja ucitava podatke o vesti (naslov, sadrzaj i komentare na vest) na news.html
# param request HttpRequest, news_id int
# return HttpResponse
# raises Http404
def news(request: HttpRequest, news_id):
    try:
        curr_news = News.objects.get(pk=news_id)
        author = User.objects.get(pk=curr_news.author.id)
        comments = Comment.objects.filter(news_id=news_id).order_by("-date_time")

        if len(comments) > 0:
            comments_with_reply = [{'comment': comment, 'comment_reply': Comment.objects.get(pk=comment.comment_reply.id) if comment.comment_reply is not None else None} for comment in comments]
        else:
            comments_with_reply = []

        context = {
            'news': curr_news,
            'author': author,
            'comments': comments_with_reply,
        }

        return render(request, 'golden_goal/news.html', context)
    except News.DoesNotExist:
        raise Http404("News not found!")


# Funkcija za azuriranje vesti ciji je id news_id
# param request HttpRequest, news_id int
# return HttpResponse, HttpResponseRedirect
# raises Http404
@login_required(login_url='sign_in')
@permission_required('golden_goal.change_news', raise_exception=True)
def update_news(request: HttpRequest, news_id):
    try:
        curr_news = News.objects.get(pk=news_id)
        user = User.objects.get(username=request.user.get_username())
        news_form = UpdateNewsForm(instance=curr_news, data=request.POST or None)

        if curr_news.author != user:
            return HttpResponse(status=403)

        if news_form.is_valid():
            curr_news.title = news_form.cleaned_data['title']
            curr_news.summary = news_form.cleaned_data['summary']
            curr_news.content = news_form.cleaned_data['content']
            curr_news.save()
            return redirect('../news/' + str(news_id))

        context = {
            'news_form': news_form
        }

        return render(request, 'golden_goal/update_news.html', context)
    except News.DoesNotExist:
        raise Http404("News not found!")


# Funkcija za brisanje vesti ciji je id news_id
# param request HttpRequest
# return HttpResponseRedirect
# raises Http404
@login_required(login_url='sign_in')
@permission_required('golden_goal.delete_news', raise_exception=True)
def delete_news(request: HttpRequest):
    try:
        news_id = request.POST['news_id']
        curr_news = News.objects.get(pk=news_id)
        user = User.objects.get(username=request.user.get_username())

        if curr_news.author != user:
            return HttpResponse(status=403)

        curr_news.delete()
        return redirect('home')
    except News.DoesNotExist:
        raise Http404("News not found!")


# Funkcija koja ucitava sve vesti na search_news.html i takodje sluzi za pretragu vesti
# po kljucnoj reci u naslovi vesti
# param request HttpRequest
# return HttpResponse
def search_news(request: HttpRequest):
    all_news = []
    query_news = []
    search_form = SearchNewsForm()

    if request.method == 'POST':
        search_form = SearchNewsForm(request.POST)

        if search_form.is_valid():
            keyword = search_form.cleaned_data['keyword']
            query_news = News.objects.filter(title__icontains=keyword)
    elif request.method == 'GET':
        query_news = News.objects.order_by('-date_time')

    for i in range(len(query_news)):
        all_news.append({
            'news': query_news[i],
            'id': i
        })

    context = {
        'all_news': all_news,
        'search_form': search_form
    }

    return render(request, 'golden_goal/search_news.html', context)


# Funkcija za dodavanje komentara na vest ciji je id news_id
# param request HttpRequest, news_id int
# return HttpResponse, HttpResponseRedirect
# raises Http404
@login_required(login_url='sign_in')
@permission_required('golden_goal.add_comment', raise_exception=True)
def comment_news(request: HttpRequest, news_id):
    try:
        curr_news = News.objects.get(pk=news_id)
        author = User.objects.get(username=request.user.get_username())
        form = CommentNews(data=request.POST or None)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.text = form.cleaned_data['text']
            comment.news_id = news_id
            comment.author_id = author.id
            comment.date_time = datetime.datetime.now()
            comment.save()
            return redirect('../news/' + str(news_id))

        context = {
            'news': curr_news,
            'author': author,
            'form': form
        }

        return render(request, 'golden_goal/comment_news.html', context)
    except News.DoesNotExist:
        raise Http404("News not found!")


# Funkcija za dodavanje komentara na komentar ciji je id comment_id
# param request HttpRequest, comment_id int
# return HttpResponse, HttpResponseRedirect
# raises Http404
@login_required(login_url='sign_in')
@permission_required('golden_goal.add_comment', raise_exception=True)
def reply_comment(request: HttpRequest, comment_id):
    try:
        curr_comm = Comment.objects.get(pk=comment_id)
        curr_news = News.objects.get(pk=curr_comm.news_id)
        author = User.objects.get(username=request.user.get_username())
        form = CommentNews(data=request.POST or None)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.text = form.cleaned_data['text']
            comment.comment_reply_id = comment_id
            comment.news_id = curr_news.id
            comment.author_id = author.id
            comment.date_time = datetime.datetime.now()
            comment.save()
            return redirect('../news/' + str(curr_news.id))

        context = {
            'news': curr_news,
            'author': author,
            'form': form
        }

        return render(request, 'golden_goal/reply_comment.html', context)
    except News.DoesNotExist:
        raise Http404("News not found!")


# Funkcija za pretvaranje obicnog korisnika u moderatora
# param request HttpRequest
# return HttpResponseRedirect
@login_required(login_url='sign_in')
@permission_required('golden_goal.change_user', raise_exception=True)
def make_moderator(request: HttpRequest):
    user_id = request.POST['user_id']

    if user_id:
        user = User.objects.get(pk=user_id)
        user.type = 'moderator'
        group_user = Group.objects.get(name='user')
        group_moderator = Group.objects.get(name='moderator')
        user.groups.remove(group_user)
        user.groups.add(group_moderator)

        for i in range(41, 47):
            image = UserImage(user=user, image=i)
            image.save()

        user.save()

    return redirect('user_administration')


# Funkcija za brisanje obicnog korisnika iz baze
# param request HttpRequest
# return HttpResponseRedirect
@login_required(login_url='sign_in')
@permission_required('golden_goal.delete_user', raise_exception=True)
def delete_user(request: HttpRequest):
    user_id = request.POST['user_id']

    if user_id:
        user = User.objects.get(pk=user_id)
        user.delete()

    return redirect('user_administration')


# Funkcija za pretvaranje moderatora u obicnog korisnika
# param request HttpRequest
# return HttpResponseRedirect
@login_required(login_url='sign_in')
@permission_required('golden_goal.change_user', raise_exception=True)
def unmake_moderator(request: HttpRequest):
    moderator_id = request.POST['moderator_id']

    if moderator_id:
        user = User.objects.get(pk=moderator_id)
        user.type = 'user'
        group_user = Group.objects.get(name='user')
        group_moderator = Group.objects.get(name='moderator')
        user.groups.add(group_user)
        user.groups.remove(group_moderator)

        for i in range(41, 47):
            filepath = "images/image_" + str(i) + ".png"

            if user.image == filepath:
                user.image = "images/image_0.png"

            image = UserImage.objects.filter(user=user, image=i)

            if image:
                image[0].delete()

        user.save()

    return redirect('user_administration')


# Funkcija za brisanje moderatora iz baze
# param request HttpRequest
# return HttpResponseRedirect
@login_required(login_url='sign_in')
@permission_required('golden_goal.delete_user', raise_exception=True)
def delete_moderator(request: HttpRequest):
    moderator_id = request.POST['moderator_id']

    if moderator_id:
        user = User.objects.get(pk=moderator_id)
        user.delete()

    return redirect('user_administration')


# Funkcija za brisanje komentara ciji je id comment_id iz baze
# param request HttpRequest, comment_id int
# return HttpResponseRedirect
# raises Http404
@login_required(login_url='sign_in')
@permission_required('golden_goal.delete_comment', raise_exception=True)
def delete_comment(request: HttpRequest, comment_id):
    try:
        curr_comm = Comment.objects.get(pk=comment_id)
        curr_news = News.objects.get(pk=curr_comm.news_id)
        author = User.objects.get(username=request.user.get_username())

        if author.type == "administrator":
            curr_comm.delete()

        return redirect('../news/' + str(curr_news.id))
    except News.DoesNotExist:
        raise Http404("Comment not found!")


# Funkcija za predvidjanje ishoda meca
# param request HttpRequest
# return HttpResponse
@login_required(login_url='sign_in')
@permission_required('golden_goal.add_prediction', raise_exception=True)
def predict_match(request: HttpRequest):
    buttons = json.loads(str(request.POST['buttons']))
    double_predictions = 0

    print(buttons)

    for button in buttons:
        info = button.split("-")
        curr_type = info[1]
        game = info[2]
        user_id = request.user.id
        predictions = Prediction.objects.filter(game=game, user_id=user_id)

        if len(predictions) > 0:
            double_predictions += 1
            curr_prediction = predictions[0]
            curr_prediction.type = curr_type + curr_prediction.type
        else:
            curr_prediction = Prediction(game=game, type=curr_type, user_id=user_id)

        curr_prediction.save()

    user = User.objects.get(username=request.user.get_username())
    user.double_prediction_counter -= double_predictions
    user.save()
    return HttpResponse(status=200)


# Funkcija za preuzimanje otvorenih poklona i ispoljavanje njihovog efekta:
# poeni - dodavanje na skor korisnika, slika - dodavanje slike u listu slika korisnika,
# duplo predvidjanje - povecavanje broja mogucih duplih predvidjanja korisnika
# param request HttpRequest
# return HttpResponse, HttpresponseRedirect
@login_required(login_url='sign_in')
def take_presents(request: HttpRequest):
    user = User.objects.get(username=request.user.get_username())

    if user.type == 'user':
        presents = Present.objects.filter(user=user)

        for present in presents:
            if present.type == 'points':
                user.score += present.points
            elif present.type == 'image':
                image = UserImage.objects.filter(user=user, image=present.image)
                if image.count() == 0:
                    user_image = UserImage(user=user, image=present.image)
                    user_image.save()
            else:
                user.double_prediction_counter += 1

            present.delete()

        user.presents -= len(presents)
        user.save()
        return redirect('user_profile')
    else:
        return HttpResponse(status=404)


# Funkcija za dobijanje mogucih duplih predvidjanja korisnika
# param request HttpRequest
# return Jsonresponse
def double_prediction_count(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse(json.dumps(0), safe=False)

    user = User.objects.get(username=request.user.get_username())
    dpc = user.double_prediction_counter
    return JsonResponse(json.dumps(dpc), safe=False)


# Funkcija za izmenu profilne slike korisnika
# param request HttpRequest
# return HttpResponseRedirect
@login_required(login_url='sign_in')
def change_profile_image(request: HttpRequest):
    user = User.objects.get(username=request.user.get_username())

    if request.method == 'POST':
        image_id = str(request.POST['change_button'])

        if image_id != '':
            user.image = 'images/image_' + image_id + '.png'
            user.save()

    return redirect('user_profile')
