import datetime

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import viewsets

from tourmarks.models import User, Location, Visit
from tourmarks.serializers import UserSerializer

import tourmarks.serializers as srz

# import rest_framework.urls


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRatioView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = srz.UserRatioSerializer(user)
        return Response(serializer.data)
        # return super().get(request, *args, **kwargs)


class UserView(generics.mixins.CreateModelMixin
               , generics.mixins.RetrieveModelMixin
               , generics.mixins.ListModelMixin
               , generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True)
    def ratio(self,request,pk,*args,**kwargs):
        user = self.get_object()
        szer = srz.UserRatioSerializer(user)
        return Response(szer.data)



class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = srz.VisitSerializer
    http_method_names = ['get']


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = srz.LocationSerializer
    http_method_names = ['get', 'post']

    @action(methods=['get'], detail=True)
    def ratio(self, request, *args, **kwargs):
        location = self.get_object()
        szer = srz.LocationRatioSerializer(location)
        return Response(szer.data)

    @action(methods=['post'], detail=True)
    def visit(self, request, *args, **kwargs):
        user = self.request.user
        location = self.get_object()
        date = datetime.datetime.now()
        visit = Visit.objects.create(**dict(user_id=user, location_id=location, date=date, ratio=0))
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
Плюсом будет:
-
использовать для авторизации jwt, подробнее тут http://jwt.io/
-
тесты
'''
