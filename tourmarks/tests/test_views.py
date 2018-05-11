import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


def create_user(sequence=1, **kwargs):
    def stuff(field, template):
        return kwargs.setdefault(field, template % (sequence))

    stuff('username', 'testuser%d')
    stuff('password', 'testpass%d')
    stuff('email', 'testuser%d@test.local')
    stuff('first_name', 'john%d')
    stuff('last_name', 'smith%d')
    kwargs.setdefault('gender', ['M', 'F'][sequence % 2])
    kwargs.setdefault('birth_date', datetime.datetime.strptime('2018-01-01', '%Y-%m-%d'))
    kwargs.setdefault('country', ['Russia', 'US', 'China', 'Germany', 'UK', 'France'][sequence % 2])
    user = User.objects.create_user(**kwargs)
    return (user, kwargs['password'])


class test_sign_in_c(APITestCase):

    def setUp(self):
        super(test_sign_in_c, self).setUp()
        self.url = reverse('sign_in')
        self.user, self.password = create_user(sequence=1)

    def test_signup_get(self):
        pass

    def test_login_post_valid(self):
        data = {
            'username': self.user.username,
            'password': self.password,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        debug = 1

    def test_login_post_invalid(self):
        data = {
            'username': self.user.username,
            'password': 'wrong_password',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_post_invalid(self):
        pass

    def test_signup_post_valid(self):
        pass

    def test_signup_post_valid(self):
        pass

    def test_signup_post_valid(self):
        pass


class test_sign_up_c(APITestCase):

    def setUp(self):
        super(test_sign_up_c, self).setUp()
        # self.user=create_user(sequence=1)
        self.url = reverse('register')

    def test_signup_post_valid(self):
        data = dict(username='john1', password='john', email='john@test.local'
                    , first_name='john', last_name='smith')
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_signup_post_invalid(self):
        data = dict(username='john2', email='john@test.local'
                    , first_name='john', last_name='smith')
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_post_valid(self):
        pass

    def test_signup_post_valid(self):
        pass

    def test_signup_post_valid(self):
        pass
