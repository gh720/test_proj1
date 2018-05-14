import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings as jwt_settings

from tourmarks.models import Location, Visit

User = get_user_model()


def generate_user_data(sequence=1, **data):
    def stuff(field, template):
        return data.setdefault(field, template % (sequence))

    stuff('username', 'testuser%d')
    stuff('password', 'testpass%d')
    stuff('email', 'testuser%d@test.local')
    stuff('first_name', 'john%d')
    stuff('last_name', 'smith%d')
    data.setdefault('gender', ['M', 'F'][sequence % 2])
    data.setdefault('birth_date', datetime.datetime.strptime('2018-01-01', '%Y-%m-%d').date())
    data.setdefault('country', ['Russia', 'US', 'China', 'Germany', 'UK', 'France'][sequence % 2])
    return data


def create_user(sequence=1, save=True, **data):
    data = generate_user_data(sequence, **data)
    if save:
        instance = User.objects.create_user(**data)
    else:
        instance = User(**data)
    instance.initial = data
    return instance


def generate_location_data(sequence=1, **data):
    def stuff(field, template):
        return data.setdefault(field, template % (sequence))

    data.setdefault('country', ['Russia', 'US', 'China', 'Germany', 'UK', 'France'][sequence % 2])
    stuff('description', 'a great place %d')
    stuff('city', 'city%d')
    stuff('name', 'name%d')
    return data


def create_location(sequence=1, save=True, **data):
    data = generate_location_data(sequence, **data)
    instance = Location(**data)
    if save:
        instance.save()
    instance.initial = data
    return instance


def generate_visit_data(sequence=1, **data):
    def stuff(field, template):
        return data.setdefault(field, template % (sequence))

    assert 'user' in data
    assert 'location' in data
    data.setdefault('date', datetime.datetime.strptime('2018-01-01', '%Y-%m-%d'))
    data.setdefault('ratio', sequence)
    return data


def create_visit(sequence=1, save=True, **data):
    data = generate_visit_data(sequence, **data)
    instance = Visit(**data)
    if save:
        instance.save()
    instance.initial = data
    return instance


class test_wrapper:
    class base_c(APITestCase):
        possible_methods = {'get', 'post', 'put', 'patch', 'delete'}

        def check_status(self, status, end_point, methods, data=None):
            data = data or {}
            for method_name in sorted(list(methods)):
                method = getattr(self.client, method_name)
                self.assertIsNotNone(method)
                response = method(end_point, data=data)
                self.assertEqual(response.status_code, status,
                                 msg="failure: endpoint %s, method %s, http:%s, expected:%s" % (
                                     end_point, method_name, response.status_code, status))

        def login(self, username, password):
            if getattr(settings, 'USE_JWT_FOR_TESTS', None):
                url = reverse('sign_in')
                response = self.client.post(url, data=dict(username=username, password=password))
                self.assertEquals(response.status_code, status.HTTP_200_OK)
                self.assertTrue('token' in response.data)
                self.client.credentials(
                    HTTP_AUTHORIZATION="%s %s" % (jwt_settings.JWT_AUTH_HEADER_PREFIX
                                                  , response.data['token']))
            else:
                self.client.login(username=self.user1.initial.get('username'),
                                  password=self.user1.initial.get('password'))
