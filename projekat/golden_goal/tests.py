from django.test import TestCase
from .models import *
from django.contrib.auth.models import Group, Permission
from bs4 import BeautifulSoup as Soup


def create_groups():
    Group.objects.create(name='administrator')
    Group.objects.create(name='moderator')
    Group.objects.create(name='user')


def create_admin():
    admin = User.objects.create_superuser(username='admin', type='administrator', password='golden_goal')
    permission = Permission.objects.get(codename='change_user')
    group_admin = Group.objects.get(name='administrator')
    group_admin.permissions.add(permission)
    admin.save()
    admin.groups.add(group_admin)
    return admin


def create_user():
    user = User(username='peraperic', type="user")
    user.set_password('pera123')
    group_user = Group.objects.get(name='user')
    user.last_login = datetime.date.today()
    user.save()
    user.groups.add(group_user)
    return user


def create_moderator():
    moderator = User(username='peraperic', type='moderator')
    moderator.set_password('pera123')
    group_moderator = Group.objects.get(name='moderator')
    moderator.last_login = datetime.datetime.now()
    moderator.save()
    moderator.groups.add(group_moderator)
    return moderator


def create_news(author, title, content):
    News.objects.create(author=author, title=title, content=content)


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


class SignUpTest(TestCase):
    def test_sign_up_success(self):
        Group.objects.create(name="user")
        Group.objects.get(name='user')

        response = self.client.post('/sign_up/', follow=True, data={
            'username': 'peraperic',
            'password1': 'sadilinikad123',
            'password2': 'sadilinikad123'
        })

        self.assertContains(response, 'Logout', html=True)

    def test_sign_up_fail_username_exists(self):
        user = User(username="dekam")
        user.set_password('sadilinikad123')
        Group.objects.create(name="user")
        group_user = Group.objects.get(name='user')
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_user)

        response = self.client.post('/sign_up/', follow=True, data={
            'username': 'dekam',
            'password1': 'sadilinikad123',
            'password2': 'sadilinikad123'
        })

        self.assertContains(response, 'A user with that username already exists.', html=True)

    def test_sign_up_fail_pass_short(self):
        Group.objects.create(name="user")
        Group.objects.get(name='user')

        response = self.client.post('/sign_up/', follow=True, data={
            'username': 'peraperic',
            'password1': 'sad',
            'password2': 'sad'
        })

        self.assertContains(response, 'This password is too short. It must contain at least 8 characters.', html=True)

    def test_sign_up_fail_pass_too_common(self):
        Group.objects.create(name="user")
        Group.objects.get(name='user')

        response = self.client.post('/sign_up/', follow=True, data={
            'username': 'peraperic',
            'password1': '12345678',
            'password2': '12345678'
        })

        self.assertContains(response, 'This password is too common.', html=True)

    def test_sign_up_fail_pass_too_similar(self):
        Group.objects.create(name="user")
        Group.objects.get(name='user')

        response = self.client.post('/sign_up/', follow=True, data={
            'username': 'peraperic',
            'password1': 'peraperic123',
            'password2': 'peraperic123'
        })

        self.assertContains(response, 'The password is too similar to the username.', html=True)

    def test_sign_up_fail_pass_all_numeric(self):
        Group.objects.create(name="user")
        Group.objects.get(name='user')

        response = self.client.post('/sign_up/', follow=True, data={
            'username': 'peraperic',
            'password1': '12345678',
            'password2': '12345678'
        })

        self.assertContains(response, 'This password is entirely numeric.', html=True)

    def test_sign_up_fail_pass_dont_match(self):
        Group.objects.create(name="user")
        Group.objects.get(name='user')

        response = self.client.post('/sign_up/', follow=True, data={
            'username': 'peraperic',
            'password1': 'peraperic123',
            'password2': 'peraperic124'
        })

        self.assertContains(response, 'The two password fields didn’t match.', html=True)

    def test_sign_up_fail_pass_not_filled(self):
        Group.objects.create(name="user")
        Group.objects.get(name='user')

        response = self.client.post('/sign_up/', follow=True, data={
            'username': 'peraperic$',
            'password1': '',
            'password2': '12345678'
        })

        self.assertContains(response, 'Registration', html=True)

    def test_sign_up_fail_pass_confirmation_not_filled(self):
        Group.objects.create(name="user")
        Group.objects.get(name='user')

        response = self.client.post('/sign_up/', follow=True, data={
            'username': 'peraperic$',
            'password1': '12345678',
            'password2': ''
        })

        self.assertContains(response, 'Registration', html=True)

    def test_sign_up_fail_username_not_filled(self):
        Group.objects.create(name="user")
        Group.objects.get(name='user')

        response = self.client.post('/sign_up/', follow=True, data={
            'username': '',
            'password1': '12345678',
            'password2': '12345678'
        })

        self.assertContains(response, 'Registration', html=True)

    def test_sign_up_fail_username_not_valid_char(self):
        Group.objects.create(name="user")
        Group.objects.get(name='user')

        response = self.client.post('/sign_up/', follow=True, data={
            'username': 'peraperic$',
            'password1': '12345678',
            'password2': '12345678'
        })

        self.assertContains(response, 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.', html=True)


class DeleteCommentTest(TestCase):
    def test_delete_comment_success(self):
        admin = User(username='kostam', type='administrator')
        admin.set_password('sadilinikad123')
        Group.objects.create(name='administrator')
        permission = Permission.objects.get(codename='delete_comment')
        group_admin = Group.objects.get(name='administrator')
        group_admin.permissions.add(permission)
        admin.last_login = datetime.datetime.now()
        admin.save()
        admin.groups.add(group_admin)

        moderator = User(username='moderator', type='moderator')
        moderator.set_password('moderator123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='add_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)
        news = News.objects.create(author=moderator, title="Test news", summary="Test news summary",
                                   content='This news will be deleted.')

        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "user"
        Group.objects.create(name="user")
        perm = Permission.objects.get(codename='add_comment')
        group_user = Group.objects.get(name='user')
        group_user.permissions.add(perm)
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_user)

        comment1 = Comment.objects.create(author=user, text="kom", news=news)
        self.client.login(username='kostam', password='sadilinikad123')

        uri = '/delete_comment/' + str(comment1.id)
        response = self.client.post(uri, follow=True, data={
            'comment_id': comment1.id
        })

        self.assertNotContains(response, 'kom', html=True)

    def test_delete_reply_comment_success(self):
        admin = User(username='kostam', type='administrator')
        admin.set_password('sadilinikad123')
        Group.objects.create(name='administrator')
        permission = Permission.objects.get(codename='delete_comment')
        group_admin = Group.objects.get(name='administrator')
        group_admin.permissions.add(permission)
        admin.last_login = datetime.datetime.now()
        admin.save()
        admin.groups.add(group_admin)

        moderator = User(username='moderator', type='moderator')
        moderator.set_password('moderator123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='add_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)
        news = News.objects.create(author=moderator, title="Test news", summary="Test news summary",
                                   content='This news will be deleted.')

        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "user"
        Group.objects.create(name="user")
        perm = Permission.objects.get(codename='add_comment')
        group_user = Group.objects.get(name='user')
        group_user.permissions.add(perm)
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_user)

        comment2 = Comment.objects.create(author=user, text="kom", news=news)
        comment1 = Comment.objects.create(author=user, text="reply", news=news, comment_reply=comment2)
        self.client.login(username='kostam', password='sadilinikad123')

        uri = '/delete_comment/' + str(comment1.id)
        response = self.client.post(uri, follow=True, data={
            'comment_id': comment1.id
        })

        self.assertNotContains(response, 'reply', html=True)

    def test_delete_comment_fail_user(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('moderator123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='add_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)
        news = News.objects.create(author=moderator, title="Test news", summary="Test news summary",
                                   content='This news will be deleted.')

        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "user"
        Group.objects.create(name="user")
        perm = Permission.objects.get(codename='add_comment')
        group_user = Group.objects.get(name='user')
        group_user.permissions.add(perm)
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_user)

        comment2 = Comment.objects.create(author=user, text="kom", news=news)
        comment1 = Comment.objects.create(author=user, text="reply", news=news, comment_reply=comment2)
        self.client.login(username='peraperic', password='sadilinikad123')

        uri = '/delete_comment/' + str(comment1.id)
        response = self.client.post(uri, follow=True, data={
            'comment_id': comment1.id
        })

        if response.status_code != 403:
            raise Exception

    def test_delete_comment_fail_moderator(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('sadilinikad123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='add_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)
        news = News.objects.create(author=moderator, title="Test news", summary="Test news summary",
                                   content='This news will be deleted.')

        user = User(username="peraperic")
        user.set_password('sadilinikad123')
        user.type = "user"
        Group.objects.create(name="user")
        perm = Permission.objects.get(codename='add_comment')
        group_user = Group.objects.get(name='user')
        group_user.permissions.add(perm)
        user.last_login = datetime.date.today()
        user.save()
        user.groups.add(group_user)

        comment2 = Comment.objects.create(author=user, text="kom", news=news)
        comment1 = Comment.objects.create(author=user, text="reply", news=news, comment_reply=comment2)
        self.client.login(username='moderator', password='sadilinikad123')

        uri = '/delete_comment/' + str(comment1.id)
        response = self.client.post(uri, follow=True, data={
            'comment_id': comment1.id
        })

        if response.status_code != 403:
            raise Exception


class AddNewsTest(TestCase):
    def test_add_news_success(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('sadilinikad123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='add_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)
        self.client.login(username='moderator', password='sadilinikad123')

        response = self.client.post('/add_news/', follow=True, data={
            'title': 'velika vest',
            'summary': 'vest',
            'content': 'velika velika vest'
        })

        self.assertContains(response, 'Logout', html=True)

    def test_add_news_fail_title(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('sadilinikad123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='add_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)
        self.client.login(username='moderator', password='sadilinikad123')

        response = self.client.post('/add_news/', follow=True, data={
            'title': '',
            'summary': 'vest',
            'content': 'velika velika vest'
        })

        self.assertContains(response, 'Create news', html=True)

    def test_add_news_fail_summary(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('sadilinikad123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='add_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)
        self.client.login(username='moderator', password='sadilinikad123')

        response = self.client.post('/add_news/', follow=True, data={
            'title': 'velika vest',
            'summary': '',
            'content': 'velika velika vest'
        })

        self.assertContains(response, 'Create news', html=True)

    def test_add_news_fail_content(self):
        moderator = User(username='moderator', type='moderator')
        moderator.set_password('sadilinikad123')
        Group.objects.create(name='moderator')
        permission = Permission.objects.get(codename='add_news')
        group_moderator = Group.objects.get(name='moderator')
        group_moderator.permissions.add(permission)
        moderator.last_login = datetime.datetime.now()
        moderator.save()
        moderator.groups.add(group_moderator)
        self.client.login(username='moderator', password='sadilinikad123')

        response = self.client.post('/add_news/', follow=True, data={
            'title': 'velika vest',
            'summary': 'vest',
            'content': ''
        })

        self.assertContains(response, 'Create news', html=True)


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

        self.client.post('/prediction/predict_match/', follow=True, data={
            'buttons': '["id-X-390305", "id-1-390310", "id-2-390302"]'
        })

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

        self.client.post('/prediction/predict_match/', follow=True, data={
            'buttons': '["id-X-390305", "id-1-390305"]'
        })

        if not Prediction.objects.filter(user=user, game=390305, type='1X').exists():
            raise Exception


class AdministrationTest(TestCase):
    def test_make_moderator(self):
        create_groups()
        admin = create_admin()
        self.client.force_login(user=admin)
        user = create_user()
        user_id = user.id

        response = self.client.post('/make_moderator', follow=True, data={
            'user_id': user_id
        })

        soup = Soup(response.content)
        self.assertIn('peraperic', soup.select('#moderator-list')[0].text)

    def test_unmake_moderator(self):
        create_groups()
        admin = create_admin()
        self.client.force_login(user=admin)
        user = create_user()
        user_id = user.id

        self.client.post('/make_moderator', follow=True, data={
            'user_id': user_id
        })

        response = self.client.post('/unmake_moderator', follow=True, data={
            'moderator_id': user_id
        })

        soup = Soup(response.content)
        self.assertNotIn('peraperic', soup.select('#moderator-list')[0].text)

    def test_delete_user(self):
        create_groups()
        admin = create_admin()
        self.client.force_login(user=admin)
        user = create_user()
        user_id = user.id

        response = self.client.post('/delete_user', follow=True, data={
            'user_id': user_id
        })

        self.assertNotContains(response, 'peraperic', html=True)

    def test_delete_moderator(self):
        create_groups()
        admin = create_admin()
        self.client.force_login(user=admin)
        moderator = create_moderator()
        user_id = moderator.id

        response = self.client.post('/delete_moderator', follow=True, data={
            'moderator_id': user_id
        })

        self.assertNotContains(response, 'peraperic', html=True)


class SearchTest(TestCase):
    def test_search_news_by_keyword_success(self):
        create_groups()
        user = create_user()
        create_news(user, "Vest1", "Sadrzaj Vest1")

        response = self.client.post("/search_news", data={
            "keyword": "Vest1"
        })

        self.assertContains(response, "Vest1")

    def test_search_news_by_keyword_fail(self):
        create_groups()
        user = create_user()
        create_news(user, "Vest1", "Sadrzaj Vest1")
        create_news(user, "Vest2", "Sadrzaj Vest2")

        response = self.client.post("/search_news", data={
            "keyword": "Vest1"
        })

        self.assertNotContains(response, "Vest2")

    def test_search_news(self):
        create_groups()
        user = create_user()
        create_news(user, "Vest1", "Sadrzaj Vest1")
        response = self.client.get("/")
        self.assertContains(response, "Vest1")

    def test_search_news_load_more(self):
        create_groups()
        user = create_user()

        for i in range(1, 5):
            create_news(user, "Vest" + str(i), "Sadrzaj Vest" + str(i))

        response = self.client.get("/")
        self.assertNotContains(response, "Vest4")
        response = self.client.get("/search_news")
        self.assertContains(response, "Vest4")


class PresentsTest(TestCase):
    def test_check_presents(self):
        create_groups()
        user = create_user()
        user.last_login = datetime.date.today() - datetime.timedelta(days=2)
        user.save()

        self.client.post("/sign_in/", follow=True, data={
            "username": "peraperic",
            "password": "pera123"
        })

        response = self.client.get("/")
        soup = Soup(response.content)
        self.assertTrue(len(soup.select('.bg-danger')) > 0)

    def test_see_presents(self):
        create_groups()
        user = create_user()
        user.last_login = datetime.date.today() - datetime.timedelta(days=2)
        user.save()

        self.client.post("/sign_in/", follow=True, data={
            "username": "peraperic",
            "password": "pera123"
        })

        response = self.client.get("/user_profile/")
        soup = Soup(response.content)
        self.assertTrue(len(soup.select('.unopened')) > 0)

    def test_open_presents(self):
        create_groups()
        user = create_user()
        user.last_login = datetime.date.today() - datetime.timedelta(days=2)
        user.save()

        self.client.post("/sign_in/", follow=True, data={
            "username": "peraperic",
            "password": "pera123"
        })

        self.client.post("/take_presents")
        response = self.client.get("/")
        soup = Soup(response.content)
        self.assertTrue(len(soup.select('.bg-success')) > 0)
