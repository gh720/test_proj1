from copy import deepcopy

from django.conf import settings
from django.contrib import auth
from rest_framework import status
from rest_framework.reverse import reverse

from tourmarks.serializers import UserSerializer

from .base_tests import User, create_user, test_wrapper


class test_register_valid_c(test_wrapper.base_c):

    def setUp(self):
        super().setUp()
        self.url = reverse('register')
        self.data = dict(username='john1', password='john', email='john@test.local'
                         , first_name='john', last_name='smith')
        self.response = self.client.post(self.url, self.data)
        self.assertEquals(self.response.status_code, status.HTTP_201_CREATED)
        self.user = auth.get_user(self.client)

    def test_availability(self):
        allowed = {'post'}
        self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, self.url, self.possible_methods - allowed)

    def test_signup_post_valid(self):
        self.assertEquals(self.response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.exists())

    def test_authenticated(self):
        self.assertTrue(self.user.is_authenticated)

    def test_register_duplicate(self):
        user_count = User.objects.count()
        response = self.client.post(self.url, data=self.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(User.objects.count(), user_count)


class test_register_invalid_c(test_wrapper.base_c):

    def setUp(self):
        super().setUp()
        self.url = reverse('register')
        self.data = dict(username='john2', email='john@test.local'
                         , first_name='john', last_name='smith')
        self.response = self.client.post(self.url, self.data)

    def test_signup_post_invalid(self):
        self.assertEquals(self.response.status_code, status.HTTP_400_BAD_REQUEST)


class test_sign_in_c(test_wrapper.base_c):

    def setUp(self):
        super().setUp()
        self.user = create_user(sequence=1)
        self.url = reverse('rest_framework:login')

    def test_availability(self):
        allowed = {'post','get','put'}
        self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, self.url, self.possible_methods - allowed)

    def test_login_post_valid(self):
        data = {
            'username': self.user.username,
            'password': self.user.initial['password'],
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_sign_in(self):
        data = {
            'username': self.user.username,
            'password': self.user.initial['password'],
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)


    def test_login_post_invalid(self):
        self.client.logout()
        data = {
            'username': self.user.username,
            'password': 'wrong_password',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


class test_users_view_c(test_wrapper.base_c):
    def setUp(self):
        super(test_users_view_c, self).setUp()
        self.user1 = create_user(sequence=1)
        self.user2 = create_user(sequence=2)

    def test_users_list(self):
        url = reverse('user_list')
        self.check_status(status.HTTP_401_UNAUTHORIZED, url, self.possible_methods - {'get'})
        response = self.client.get(url)
        self.assertEquals(len(response.data), 2)

    def test_users_post_anon(self):
        url = reverse('user_details', kwargs=dict(pk=1))
        self.check_status(status.HTTP_401_UNAUTHORIZED, url, self.possible_methods - {'get','post'})
        self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, {'post'})


class test_users_view_authd_c(test_wrapper.base_c):
    def setUp(self):
        super(test_users_view_authd_c, self).setUp()
        self.user1 = create_user(sequence=1)
        self.user2 = create_user(sequence=2)
        self.user3 = create_user(sequence=3, save=False)
        self.user4 = create_user(sequence=4, save=False)
        self.login(username=self.user1.initial.get('username'), password=self.user1.initial.get('password'))
        self.szr2 = UserSerializer(self.user2)

    def test_users_post(self):
        url = reverse('user_list')
        self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, self.possible_methods - {'get'})

    def test_modify_elses(self):
        url = reverse('user_details', kwargs=dict(pk=self.user2.id))
        self.check_status(status.HTTP_403_FORBIDDEN, url, self.possible_methods - {'get', 'post'})

    def test_users_update_put_nonexistent(self): # drf 3.0 -> 404
        url = reverse('user_details', kwargs=dict(pk=99))
        response = self.client.put(url, data=self.user4.initial)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_update_put(self):
        url = reverse('user_details', kwargs=dict(pk=self.user1.id))
        new_data = deepcopy(self.user1.initial)
        old_pass = self.user1.password
        new_data['email'] = 'update1@test.local'
        response = self.client.put(url, data=new_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEquals(self.user1.email, new_data['email'])
        self.assertEquals(self.user1.password, old_pass)

    def test_users_update_patch(self):
        url = reverse('user_details', kwargs=dict(pk=self.user1.id))
        new_data = {'email': 'update2@test.local'}
        old_pass = self.user1.password
        response = self.client.patch(url, data=new_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEquals(self.user1.email, new_data['email'])
        self.assertEquals(self.user1.password, old_pass)

if getattr(settings,'USE_JWT_FOR_TESTS',None):
    class test_users_view_authd_no_creds_c(test_wrapper.base_c):
        def setUp(self):
            super().setUp()
            self.user1 = create_user(sequence=1)
            self.login(username=self.user1.initial.get('username'), password=self.user1.initial.get('password'))

        def test_users_update_no_creds(self):
            url = reverse('user_details', kwargs=dict(pk=self.user1.id))
            new_data = {'email': 'update2@test.local'}
            self.client.credentials()
            response = self.client.patch(url, data=new_data)
            self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class test_users_view_authd_delete_c(test_wrapper.base_c):
    def setUp(self):
        super().setUp()
        self.user1 = create_user(sequence=1)
        self.user2 = create_user(sequence=2)
        self.client.login(username=self.user1.initial.get('username'), password=self.user1.initial.get('password'))

    def test_users_delete(self):
        url = reverse('user_details', kwargs=dict(pk=self.user2.id))
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('user_details', kwargs=dict(pk=self.user1.id))
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('user_list')
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
