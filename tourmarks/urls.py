from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as rfa_views
from tourmarks.views import UserCreate, UserListView, UserDetailView, LocationViewSet, VisitViewSet, UserRatioView

# app_name = 'api'

router = routers.SimpleRouter()
router.register(r'locations', LocationViewSet)
router.register('visits', VisitViewSet)

urlpatterns = [
    url('register/', UserCreate.as_view(), name='register')
    , url('sign_in/', rfa_views.obtain_auth_token, name='sign_in')
    , url('users/', UserListView.as_view(), name='user_list')
    , url('users/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user_details')
    , url('users/(?P<pk>\d+)/ratio/$', UserRatioView.as_view(), name='user_ratio')
]

urlpatterns += router.urls
