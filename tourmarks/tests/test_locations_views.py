import unittest
from copy import deepcopy

from django.forms import model_to_dict
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from tourmarks.models import Location
from tourmarks.serializers import UserSerializer

from .base_tests import User, generate_user_data, create_user, test_wrapper, generate_location_data, create_location


def test_list(self):
    url = reverse('locations')
    self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, self.possible_methods - {'get', 'post'})


def test_post_anon(self):
    url = reverse('locations')
    self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, self.possible_methods - {'get', 'post'})


class locations_test_base_c(test_wrapper.base_c):
    def setUp(self):
        self.location1 = create_location(sequence=1, country='Russia')
        self.location2 = create_location(sequence=2, country='US')
        self.user1 = create_user(sequence=1)


class test_locations_views_c(locations_test_base_c):

    def setUp(self):
        super(test_locations_views_c, self).setUp()

    def test_locations_list(self):
        url = reverse('location-list')
        self.check_status(status.HTTP_401_UNAUTHORIZED, url, self.possible_methods - {'get', 'post'})
        self.check_status(status.HTTP_401_UNAUTHORIZED, url, {'post'})
        response = self.client.get(url)
        self.assertEquals(len(response.data), 2)

    def test_locations_post_anon(self):
        url = reverse('location-detail', kwargs=dict(pk=self.location1.id))
        self.check_status(status.HTTP_401_UNAUTHORIZED, url, self.possible_methods - {'get'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get('country'), 'Russia')


class test_locations_view_authd_c(locations_test_base_c):
    def setUp(self):
        super(test_locations_view_authd_c, self).setUp()
        self.data3 = generate_location_data(sequence=3)
        self.client.login(username=self.user1.initial.get('username'), password=self.user1.initial.get('password'))

    def test_locations_post(self):
        url = reverse('location-list')
        self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, self.possible_methods - {'get', 'post'})
        location_count = Location.objects.count()
        response = self.client.post(url, data=self.data3)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Location.objects.count(), location_count + 1)

    def test_locations_update_put(self):
        url = reverse('location-detail', kwargs=dict(pk=self.location1.id))
        new_data = deepcopy(model_to_dict(self.location1))
        new_data['description'] = 'not so great a place'
        response = self.client.put(url, data=new_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.location1.refresh_from_db()
        self.assertEquals(self.location1.description, new_data['description'])

    def test_locations_update_patch(self):
        url = reverse('location-detail', kwargs=dict(pk=self.location1.id))
        new_data = {'description': 'not so great a place'}
        response = self.client.patch(url, data=new_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.location1.refresh_from_db()
        self.assertEquals(self.location1.description, new_data['description'])


class test_location_view_authd_delete_c(locations_test_base_c):
    def setUp(self):
        super(test_location_view_authd_delete_c, self).setUp()
        self.client.login(username=self.user1.initial.get('username'), password=self.user1.initial.get('password'))

    def test_location_delete(self):
        url = reverse('location-detail', kwargs=dict(pk=99))
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEquals(Location.objects.count(), 2)
        url = reverse('location-detail', kwargs=dict(pk=self.location1.id))
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Location.objects.count(), 1)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(Location.objects.count(), 1)