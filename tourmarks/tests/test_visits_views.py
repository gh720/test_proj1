from copy import deepcopy

from django.forms import model_to_dict
from rest_framework import status
from rest_framework.reverse import reverse

from tourmarks.models import Visit
from tourmarks.tests.test_locations_views import locations_test_base_c
from .base_tests import create_user, test_wrapper, create_location, create_visit


def test_list(self):
    url = reverse('visit-list')
    self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, self.possible_methods - {'get', 'post'})


def test_post_anon(self):
    url = reverse('visit-list')
    self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, self.possible_methods - {'get', 'post'})


class visits_test_wrapper:
    class base_c(test_wrapper.base_c):
        def setUp(self):
            self.location1 = create_location(sequence=1, country='Russia')
            self.location2 = create_location(sequence=2, country='US')
            self.user1 = create_user(sequence=1)
            self.user2 = create_user(sequence=2)
            self.visit1 = create_visit(sequence=1, location=self.location1, user=self.user1, ratio=10)
            self.visit2 = create_visit(sequence=2, location=self.location2, user=self.user2)
            self.visit3 = create_visit(sequence=3, save=False, location=self.location1, user=self.user1)


class test_visits_views_c(visits_test_wrapper.base_c):

    def setUp(self):
        super().setUp()

    def test_visits_list(self):
        url = reverse('visit-list')
        self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, self.possible_methods - {'get'})
        response = self.client.get(url)
        self.assertEquals(len(response.data), 2)

    def test_visits_post_anon(self):
        url = reverse('visit-detail', kwargs=dict(pk=self.visit1.id))
        self.check_status(status.HTTP_401_UNAUTHORIZED, url, self.possible_methods - {'get', 'post'})
        self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, {'post'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['ratio'], 10)


class test_visits_view_authd_c(visits_test_wrapper.base_c):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.user1.initial.get('username'), password=self.user1.initial.get('password'))

    def test_visits_post(self):
        url = reverse('location-visit', kwargs=dict(pk=self.location1.id))
        self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, self.possible_methods - {'get', 'post'})
        visit_count = Visit.objects.count()
        data = model_to_dict(self.visit3)
        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Visit.objects.count(), visit_count + 1)

    def test_modify_elses(self):
        url = reverse('visit-detail', kwargs=dict(pk=self.visit2.id))
        self.check_status(status.HTTP_403_FORBIDDEN, url, self.possible_methods - {'get', 'post'})

    def test_visits_update_put(self):
        url = reverse('visit-detail', kwargs=dict(pk=self.visit1.id))
        new_data = deepcopy(model_to_dict(self.visit1))
        new_data['ratio'] = 11
        response = self.client.put(url, data=new_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(str(response.data['ratio'][0]).index('Ensure this value is less than or equal') >= 0)
        new_data['ratio'] = 8
        response = self.client.put(url, data=new_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.visit1.refresh_from_db()
        self.assertEquals(self.visit1.ratio, new_data['ratio'])

    def test_visits_update_patch(self):
        url = reverse('visit-detail', kwargs=dict(pk=self.location1.id))
        new_data = {'ratio': 11}
        response = self.client.patch(url, data=new_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(str(response.data['ratio'][0]).index('Ensure this value is less than or equal') >= 0)
        new_data = {'ratio': 9}
        response = self.client.patch(url, data=new_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.visit1.refresh_from_db()
        self.assertEquals(self.visit1.ratio, new_data['ratio'])


class test_visits_view_authd_delete_c(visits_test_wrapper.base_c):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.user1.initial.get('username'), password=self.user1.initial.get('password'))

    def test_visit_delete(self):
        url = reverse('visit-detail', kwargs=dict(pk=99))
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEquals(Visit.objects.count(), 2)
        url = reverse('visit-detail', kwargs=dict(pk=self.visit1.id))
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Visit.objects.count(), 1)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(Visit.objects.count(), 1)


class test_ratio_view_c(locations_test_base_c):
    def setUp(self):
        super().setUp()
        self.user2 = create_user(sequence=2)
        self.visit1 = create_visit(sequence=1, location=self.location1, user=self.user1, ratio=5)
        self.visit2 = create_visit(sequence=2, location=self.location2, user=self.user2, ratio=6)
        self.visit3 = create_visit(sequence=3, location=self.location1, user=self.user2, ratio=9)

    def test_location_ratio_nonexistent(self):
        url = reverse('location-ratio', kwargs=dict(pk=99))
        self.check_status(status.HTTP_401_UNAUTHORIZED, url, self.possible_methods - {'get'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_ratio_nonexistent(self):
        url = reverse('user_ratio', kwargs=dict(pk=99))
        self.check_status(status.HTTP_405_METHOD_NOT_ALLOWED, url, self.possible_methods - {'get'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_location_ratio(self):
        url = reverse('location-ratio', kwargs=dict(pk=self.location1.id))
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.data
        visitors = data.pop('visitors')
        ids = {user['id'] for user in visitors}
        data.pop('visits', None)
        self.assertEquals(len(visitors), 2)
        self.assertDictEqual(data, dict(count=2, avg=7))
        self.assertSetEqual(ids, {self.user1.id, self.user2.id})

    def test_user_ratio(self):
        url = reverse('user_ratio', kwargs=dict(pk=self.user2.id))
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.data
        locations = data.pop('locations')
        ids = {location['id'] for location in locations}
        data.pop('visits', None)
        self.assertEquals(len(locations), 2)
        self.assertDictEqual(data, dict(count=2, avg=7.5))
        self.assertSetEqual(ids, {self.location1.id, self.location2.id})
