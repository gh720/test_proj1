import datetime

from django.contrib.auth import authenticate, login
from rest_framework import generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from tourmarks.models import User, Location, Visit
from tourmarks.serializers import UserSerializer

import tourmarks.serializers as srz

class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    Granting object permissions: a model's object_owner property should match request.user
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj.object_owner == request.user

class UserListView(generics.ListAPIView):
    '''
    List of users ('user_list')
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    User details ('user_details')
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,  )


class UserCreateView(generics.CreateAPIView):
    '''
    Register a user ('register')
    '''
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_ = serializer.save()
        user = authenticate(username=user_.username, password=request.data.get('password'))
        login(request, user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserRatioView(generics.RetrieveAPIView):
    '''
    Rating for a user ('users')
    '''
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = srz.UserRatioSerializer(user)
        return Response(serializer.data)

class VisitViewSet(viewsets.ModelViewSet):
    '''
    Endpoints for a visit ('visits')
    '''
    queryset = Visit.objects.all()
    serializer_class = srz.VisitSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    permission_classes = (IsOwnerOrReadOnly,)


class LocationViewSet(viewsets.ModelViewSet):
    '''
    Endpoints for a location ('locations')
    '''
    queryset = Location.objects.all()
    serializer_class = srz.LocationSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(methods=['get'], detail=True)
    def ratio(self, request, *args, **kwargs):
        '''
        Average rating for a location ('location')
        '''
        location = self.get_object()
        szer = srz.LocationRatioSerializer(location)
        return Response(szer.data)

    @action(methods=['post'], detail=True)
    def visit(self, request, *args, **kwargs):
        '''
        posting a visit info (/locations/{id}/visit)
        expects: self.request.data to be a json, where rating is a number from 1 to 10:
            { "ratio": rating }
        '''
        user = self.request.user
        location = self.get_object()
        date = datetime.datetime.now()
        visit = Visit.objects.create(**dict(user=user, location=location, date=date, ratio=0))
        serializer = srz.VisitSerializer(visit, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
Запросы:
| endpoint | GET | POST | PUT|PATCH | DELETE |
|:---------------------:|:-----------------------------------------------------------:|:-------------------------:|:---------:|:--------:
|
| /register | - | Регистрация пользователя | - | - |
| /sign_in | - | Авторизация пользователя | - | - |
| /users | Список пользователей | - | - | - |
| /users/<id> | Информация о пользователе | - | Изменение | Удаление |
| /locations | Список достопримечательностей | Создание нового места | - | - |
| /locations/<id> | Информация о достопримечательности | - | Изменение | Удаление |
| /locations/<id>/visit | - | Отметиться в данном месте | - | - |
| /locations/<id>/ratio | Получение информации о текущих рейтингах | - | - | - |
| /visits | Список посещений | - | - | - |
| /visits/<id> | Информация о посещении | - | Изменение | Удаление |
| /users/<id>/ratio | Информация о посещениях пользователя и поставленных оценках | - | - | - |
Примеры запросов:
post /locations/<id>/visit BODY {"ratio": 6} (все остальные данные собираются автоматом, дата 
текущая, пользоватил - кто отправил запрос, место определено в endpoint`е)
get /users/<id>/ratio RESPONSE {"count": 17, "avg": 6.7, "locations": [{"id": 1, ...}, ...]}
get /locations/<id>/ratio RESPONSE {"count": 5, "avg": 8.7, "visitors": [{"id": 1, ...}, ...]}
'''
