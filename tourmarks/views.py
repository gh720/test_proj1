from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from tourmarks.models import User, Location, Visit
from tourmarks.serializers import UserSerializer

import tourmarks.serializers as srz

import rest_framework.urls


class UserListView(generics.ListAPIView):
    # def get(self, request):
    #     users = User.objects.all()[:10]
    #     data = UserSerializer(users, many=True).data
    #     return Response(data)

    queryset= User.objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset= User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = srz.VisitSerializer
    http_method_names = ['get']


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = srz.LocationSerializer
    http_method_names = ['get']

    @action(methods=['get'], detail=True)
    def ratio(self):
        location = self.get_object()
        szer = srz.LocationRatioSerializer(location)
        return Response(szer.data)


class UserRatioView(generics.GenericAPIView):
    serializer_class = srz.UserRatioSerializer

    @action(methods=['get'], detail=True)
    def ratio(self):
        user = self.get_object()
        szer = srz.UserRatioSerializer(user)
        return Response(szer.data)



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
Плюсом будет:
-
использовать для авторизации jwt, подробнее тут http://jwt.io/
-
тесты
'''
