from django.test import TestCase
from .models import *
from django.contrib.auth.models import Group, Permission


class SigninTest(TestCase):
    def test_sign_in_success(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        Group.objects.create(name="user")
        group_user = Group.objects.get(name='user')
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_user)

        response = self.client.post('/sign_in/', follow=True, data={
            'username': 'peraperic',
            'password': 'sadilinikad123'
        })

        self.assertContains(response, 'Logout', html=True)

    def test_sign_in_fail_user(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        Group.objects.create(name="user")
        group_user = Group.objects.get(name='user')
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_user)

        response = self.client.post('/sign_in/', follow=True, data={
            'username': 'pera',
            'password': 'sadilinikad123'
        })

        self.assertContains(response, 'Fail login', html=True)

    def test_sign_in_fail_pass(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        Group.objects.create(name="user")
        group_user = Group.objects.get(name='user')
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_user)

        response = self.client.post('/sign_in/', follow=True, data={
            'username': 'peraperic',
            'password': 'nowornever123'
        })

        self.assertContains(response, 'Fail login', html=True)


class NewsEditTest(TestCase):
    def test_news_edit(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "moderator"
        Group.objects.create(name="moderator")
        perm = Permission.objects.get(codename='change_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(perm)
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja")
        self.client.login(username='peraperic', password='sadilinikad123')
        uri = '/update_news/' + str(news.id)

        response = self.client.post(uri, follow=True, data={
            'title': 'Novi naslov vesti',
            'summary': 'Testiranje funkcionalnosti',
            'content': 'Kontent nakon update'
        })

        self.assertContains(response, 'Novi naslov vesti', html=True)
        self.assertContains(response, 'Kontent nakon update', html=True)

    def test_news_edit_not_moderator(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "user"
        Group.objects.create(name="user")
        group_moderator = Group.objects.get(name='user')
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja")
        self.client.login(username='peraperic', password='sadilinikad123')
        uri = '/update_news/' + str(news.id)

        response = self.client.post(uri, follow=True, data={
            'title': 'Novi naslov vesti',
            'summary': 'Testiranje funkcionalnosti',
            'content': 'Kontent nakon update'
        })

        if response.status_code != 403:
            raise Exception

    def test_news_edit_not_author(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "moderator"
        Group.objects.create(name="moderator")
        perm = Permission.objects.get(codename='change_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(perm)
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja")
        user = User(username="perapericdva")
        user.set_password('sadilinikad123')
        user.type = "moderator"
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        self.client.login(username='perapericdva', password='sadilinikad123')
        uri = '/update_news/' + str(news.id)

        response = self.client.post(uri, follow=True, data={
            'title': 'Novi naslov vesti',
            'summary': 'Testiranje funkcionalnosti',
            'content': 'Kontent nakon update'
        })

        if response.status_code != 403:
            raise Exception


class CommentNewsTest(TestCase):
    def test_comment_news(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "user"
        Group.objects.create(name="user")
        perm = Permission.objects.get(codename='add_comment')
        group_moderator = Group.objects.get(name='user')
        group_moderator.permissions.add(perm)
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja")
        self.client.login(username='peraperic', password='sadilinikad123')
        uri = '/comment_news/' + str(news.id)

        response = self.client.post(uri, follow=True, data={
            'text': 'Novi komentar'
        })

        self.assertContains(response, 'Novi komentar', html=True)

    def test_comment_news_no_perm(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "moderator"
        Group.objects.create(name="moderator")
        group_moderator = Group.objects.get(name='moderator')
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja")
        self.client.login(username='peraperic', password='sadilinikad123')
        uri = '/comment_news/' + str(news.id)

        response = self.client.post(uri, follow=True, data={
            'text': 'Novi komentar'
        })

        if response.status_code != 403:
            raise Exception

    def test_replying_comments(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "user"
        Group.objects.create(name="user")
        perm = Permission.objects.get(codename='add_comment')
        group_moderator = Group.objects.get(name='user')
        group_moderator.permissions.add(perm)
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja")
        comm = Comment.objects.create(author=user, text="Originalni komentar", news=news)
        self.client.login(username='peraperic', password='sadilinikad123')
        uri = '/reply_comment/' + str(comm.id)

        response = self.client.post(uri, follow=True, data={
            'text': 'Novi komentar'
        })

        self.assertContains(response, 'Novi komentar', html=True)

    def test_replying_comments_no_perm(self):
        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "moderator"
        Group.objects.create(name="moderator")
        group_moderator = Group.objects.get(name='moderator')
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_moderator)
        news = News.objects.create(author=user, title="Naslov vesti", summary="Testiranje funkcionalnosti", content="Kontent nakon kreiranja")
        comm = Comment.objects.create(author=user, text="Originalni komentar", news=news)
        self.client.login(username='peraperic', password='sadilinikad123')
        uri = '/reply_comment/' + str(comm.id)

        response = self.client.post(uri, follow=True, data={
            'text': 'Novi komentar'
        })

        if response.status_code != 403:
            raise Exception


class ModeratorAuthorizationTest(TestCase):
    def test_moderator_authorization_success(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('moderator123')
        Group.objects.create(name='moderator')
        group_moderator = Group.objects.get(name='moderator')
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)

        response = self.client.post('/sign_in/', follow=True, data={
            'username': 'moderator',
            'password': 'moderator123'
        })

        self.assertContains(response, 'Add news', html=True)

    def test_moderator_authorization_fail_username(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('moderator123')
        Group.objects.create(name='moderator')
        group_moderator = Group.objects.get(name='moderator')
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)

        response = self.client.post('/sign_in/', follow=True, data={
            'username': 'mod',
            'password': 'moderator123'
        })

        self.assertContains(response, 'Fail login', html=True)

    def test_moderator_authorization_fail_password(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('moderator123')
        Group.objects.create(name='moderator')
        group_moderator = Group.objects.get(name='moderator')
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)

        response = self.client.post('/sign_in/', follow=True, data={
            'username': 'moderator',
            'password': '123'
        })

        self.assertContains(response, 'Fail login', html=True)


class DeleteNewsTest(TestCase):
    def test_delete_news_success(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('moderator123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='delete_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)
        news = News.objects.create(author=moderator, title="Test news", summary="Test news summary", content='This news will be deleted.')
        self.client.login(username='moderator', password='moderator123')

        response = self.client.post('/delete_news', follow=True, data={
            'news_id': news.id
        })

        self.assertNotContains(response, 'Test news', html=True)

    def test_delete_news_fail_not_moderator(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('moderator123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='delete_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)

        user = User(username='user', type='user')
        user.set_password('user123')
        Group.objects.create(name='user')
        group_user = Group.objects.get(name='user')
        user.last_login = datetime.datetime.now()
        user.save()
        user.groups.add(group_user)
        news = News.objects.create(author=moderator, title="Test news", summary="Test news summary", content='This news will be deleted.')
        self.client.login(username='user', password='user123')

        response = self.client.post('/delete_news', follow=True, data={
            'news_id': news.id
        })

        if response.status_code != 403:
            raise Exception

    def test_delete_news_fail_not_author(self):
        moderator1 = User(username='moderator1', type='moderator')
        moderator1.set_password('moderator1123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='delete_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator1.last_login = datetime.datetime.now()
        moderator1.save()
        moderator1.groups.add(group_moderator)

        moderator2 = User(username='moderator2', type='moderator')
        moderator2.set_password('moderator2123')
        moderator2.last_login = datetime.datetime.now()
        moderator2.save()
        moderator2.groups.add(group_moderator)
        news = News.objects.create(author=moderator1, title="Test news", summary="Test news summary", content='This news will be deleted.')
        self.client.login(username='moderator2', password='moderator2123')

        response = self.client.post('/delete_news', follow=True, data={
            'news_id': news.id
        })

        if response.status_code != 403:
            raise Exception


class PredictionTest(TestCase):
    def test_add_prediction_success(self):
        user = User(username='user', type='user')
        user.set_password('user123')
        Group.objects.create(name='user')
        permission = Permission.objects.get(codename='add_prediction')
        group_user = Group.objects.get(name='user')
        group_user.permissions.add(permission)
        user.last_login = datetime.datetime.now()
        user.save()
        user.groups.add(group_user)
        self.client.login(username='user', password='user123')

        response = self.client.post('/prediction/predict_match', follow=False, data={
            'buttons': ["id-X-390305", "id-1-390310", "id-2-390302"]
        })

        print(response.status_code)
        print(Prediction.objects.all())

        if not Prediction.objects.filter(user=user, game=390305, type='X').exists():
            raise Exception

        if not Prediction.objects.filter(user=user, game=390310, type='1').exists():
            raise Exception

        if not Prediction.objects.filter(user_id=user.id, game=390302, type='2').exists():
            raise Exception

    def test_add_double_prediction_success(self):
        user = User(username='user', type='user')
        user.set_password('user123')
        Group.objects.create(name='user')
        permission = Permission.objects.get(codename='add_prediction')
        group_user = Group.objects.get(name='user')
        group_user.permissions.add(permission)
        user.last_login = datetime.datetime.now()
        user.double_prediction_counter = 1
        user.save()
        user.groups.add(group_user)
        self.client.login(username='user', password='user123')

        response = self.client.post('/prediction/predict_match', follow=False, data={
            'buttons': ["id-X-390305", "id-1-390305"]
        })

        print(response.status_code)
        print(Prediction.objects.all())

        if not Prediction.objects.filter(user=user, game=390305, type='X').exists():
            raise Exception

        if not Prediction.objects.filter(user=user, game=390305, type='1').exists():
            raise Exception
