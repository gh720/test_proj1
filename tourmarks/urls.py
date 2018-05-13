from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as rfa_views
from rest_framework.routers import DefaultRouter
import rest_framework.urls as drf_urls

from tourmarks.views import LocationViewSet, VisitViewSet, UserCreateView, UserDetailView, UserRatioView, \
    UserListView

# app_name = 'api'


# location_list=LocationViewSet

router = routers.SimpleRouter()
router.register('locations', LocationViewSet)
router.register('visits', VisitViewSet)

urlpatterns = [
    url('^register/$', UserCreateView.as_view(), name='register')
    , url('^sign_in/$', rfa_views.obtain_auth_token, name='sign_in')
    , url('users/$', UserListView.as_view(), name='user_list')
    , url('users/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user_details')
    , url('users/(?P<pk>\d+)/ratio/$', UserRatioView.as_view(), name='user_ratio')
]

urlpatterns += router.urls
