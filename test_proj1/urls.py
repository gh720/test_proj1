from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from rest_framework_swagger.views import get_swagger_view
from django.urls import path, include

schema_view = get_swagger_view(title='API docs')

urlpatterns = [
    url(r'^admin/', admin.site.urls)
    # , url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login')
    # , url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout')
    , url(r'^auth/', include('rest_framework.urls'))
    , url(r'^docs/', schema_view)
    , url(r'^', include('tourmarks.urls'))
    # , path(r'api/', tourmarks.urls)
    ,
]
