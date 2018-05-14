import rest_framework_jwt.views
from django.conf.urls import url
from rest_framework import routers

from tourmarks.views import LocationViewSet, VisitViewSet, UserCreateView, UserDetailView, UserRatioView, \
    UserListView

router = routers.SimpleRouter()
router.register('locations', LocationViewSet)
router.register('visits', VisitViewSet)

urlpatterns = [
    url('^register/$', UserCreateView.as_view(), name='register')
    , url(r'^sign_in/', rest_framework_jwt.views.obtain_jwt_token, name='sign_in')
    , url('users/$', UserListView.as_view(), name='user_list')
    , url('users/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user_details')
    , url('users/(?P<pk>\d+)/ratio/$', UserRatioView.as_view(), name='user_ratio')
]

urlpatterns += router.urls
