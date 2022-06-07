import datetime

from django.test import TestCase

# Create your tests here.

from .models import *
from django.contrib.auth.models import Group,Permission, ContentType

class SigninTest(TestCase):

    def test_sign_in_success(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        Group.objects.create(name="user")
        group_user = Group.objects.get(name='user')
        user.last_login= datetime.date.today()
        user.save()
        user.groups.add(group_user)
        response = self.client.post('/sign_in/',follow = True, data={
            'username': 'peraperic',
            'password': 'sadilinikad123'
        })
        self.assertContains(response,'Logout', html=True)

    def test_sign_in_failuser(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        Group.objects.create(name="user")
        group_user = Group.objects.get(name='user')
        user.last_login= datetime.date.today()
        user.save()
        user.groups.add(group_user)
        response = self.client.post('/sign_in/',follow = True, data={
            'username': 'pera',
            'password': 'sadilinikad123'
        })
        self.assertContains(response,'Fail login', html=True)

    def test_sign_in_failpass(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        Group.objects.create(name="user")
        group_user = Group.objects.get(name='user')
        user.last_login= datetime.date.today()
        user.save()
        user.groups.add(group_user)
        response = self.client.post('/sign_in/',follow = True, data={
            'username': 'peraperic',
            'password': 'nowornever123'
        })
        self.assertContains(response,'Fail login', html=True)

class NewsEditTest(TestCase):

    def test_news_edit(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type="moderator"
        Group.objects.create(name="moderator")
        cont = ContentType.objects.get_for_model(News)
        perm = Permission.objects.get(codename='change_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(perm)
        user.last_login= datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja" )
        log =self.client.login(username='peraperic', password='sadilinikad123')
        uri='/update_news/' + str(news.id)
        response = self.client.post(uri, follow = True, data={
            'title': 'Novi naslov vesti',
            'summary': 'Testiranje funkcionalnosti',
            'content': 'Kontent nakon update'
        })
        self.assertContains(response,'Novi naslov vesti', html=True)
        self.assertContains(response,'Kontent nakon update', html=True)

    def test_news_edit_notmoderator(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type="user"
        Group.objects.create(name="user")
        cont = ContentType.objects.get_for_model(News)
        group_moderator = Group.objects.get(name='user')
        user.last_login= datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja" )
        log =self.client.login(username='peraperic', password='sadilinikad123')
        uri='/update_news/' + str(news.id)
        response = self.client.post(uri, follow = True, data={
            'title': 'Novi naslov vesti',
            'summary': 'Testiranje funkcionalnosti',
            'content': 'Kontent nakon update'
        })
        if (response.status_code!=403):
            raise Exception

    # def test_news_edit_notauthor(self):
    #     user = User(username="peraperic")
    #     user.set_password('sadilinikad123')
    #     user.type="moderator"
    #     Group.objects.create(name="moderator")
    #     cont = ContentType.objects.get_for_model(News)
    #     perm = Permission.objects.get(codename='change_news')
    #     group_moderator = Group.objects.get(name='moderator')
    #     group_moderator.permissions.add(perm)
    #     user.last_login= datetime.date.today()
    #     user.save()
    #     user.groups.add(group_moderator)
    #     news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja" )
    #     user = User(username="perapericdva")
    #     user.set_password('sadilinikad123')
    #     user.type = "moderator"
    #     user.last_login = datetime.date.today()
    #     user.save()
    #     user.groups.add(group_moderator)
    #     log =self.client.login(username='perapericdva', password='sadilinikad123')
    #     uri='/update_news/' + str(news.id)
    #     response = self.client.post(uri, follow = True, data={
    #         'title': 'Novi naslov vesti',
    #         'summary': 'Testiranje funkcionalnosti',
    #         'content': 'Kontent nakon update'
    #     })
    #     if (response.status_code != 403):
    #         print(response.status_code)
    #         raise Exception


class CommentNewsTest(TestCase):

    def test_comment_news(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type="user"
        Group.objects.create(name="user")
        cont = ContentType.objects.get_for_model(News)
        perm = Permission.objects.get(codename='add_comment')
        group_moderator = Group.objects.get(name='user')
        group_moderator.permissions.add(perm)
        user.last_login= datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja" )
        log =self.client.login(username='peraperic', password='sadilinikad123')
        uri='/comment_news/' + str(news.id)
        response = self.client.post(uri, follow = True, data={
            'text': 'Novi komentar'
        })
        self.assertContains(response,'Novi komentar', html=True)

    def test_comment_news_noperm(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type="moderator"
        Group.objects.create(name="moderator")
        group_moderator = Group.objects.get(name='moderator')
        user.last_login= datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja" )
        log =self.client.login(username='peraperic', password='sadilinikad123')
        uri='/comment_news/' + str(news.id)
        response = self.client.post(uri, follow = True, data={
            'text': 'Novi komentar'
        })
        if (response.status_code != 403):
            raise Exception

    def test_replying_comments(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type="user"
        Group.objects.create(name="user")
        cont = ContentType.objects.get_for_model(News)
        perm = Permission.objects.get(codename='add_comment')
        group_moderator = Group.objects.get(name='user')
        group_moderator.permissions.add(perm)
        user.last_login= datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja" )
        comm = Comment.objects.create(author=user, text="Originalni komentar", news=news)
        log =self.client.login(username='peraperic', password='sadilinikad123')
        uri='/reply_comment/' + str(comm.id)
        response = self.client.post(uri, follow = True, data={
            'text': 'Novi komentar'
        })
        self.assertContains(response,'Novi komentar', html=True)

    def test_replying_comments_noperm(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type="moderator"
        Group.objects.create(name="moderator")
        group_moderator = Group.objects.get(name='moderator')
        user.last_login= datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja" )
        comm = Comment.objects.create(author=user, text="Originalni komentar", news=news)
        log =self.client.login(username='peraperic', password='sadilinikad123')
        uri='/reply_comment/' + str(comm.id)
        response = self.client.post(uri, follow = True, data={
            'text': 'Novi komentar'
        })
        if (response.status_code != 403):
            raise Exception
