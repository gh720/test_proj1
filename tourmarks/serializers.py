from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.decorators import detail_route, action

from tourmarks.models import User, Visit, Location


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'birth_date', 'country', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'],
                    first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                    gender=validated_data['gender'], birth_date=validated_data['birth_date'],
                    country=validated_data['country'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        exclude = []

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = []

class UserRatioSerializer(serializers.Serializer):

    def to_representation(self, instance):
        '''
         {"count": 17, "avg": 6.7, "locations": [{"id": 1, ...}, ...]}
        :return:
        '''
        qs = Visit.objects.filter(user=instance).select_related('location')
        # visit_szr = VisitSerializer()
        stats = dict(count=0, avg=0, locations=[], visits=[])
        rating_sum = 0
        for item in qs:
            stats['count']+=1
            rating_sum+=item.ratio
            stats['locations'].append(LocationSerializer(item.location).data)
            stats['visits'].append(VisitSerializer(item).data)
        if stats['count']>0:
            stats['avg']=rating_sum/stats['count']
        return stats





class LocationRatioSerializer(serializers.Serializer):

    def to_representation(self, instance):
        '''
         {"count": 17, "avg": 6.7, "locations": [{"id": 1, ...}, ...]}
        :return:
        '''
        qs = Visit.objects.filter(location=instance).select_related('user')
        # QuerySet.select_related()
        # visit_szr = VisitSerializer()
        stats = dict(count=0, avg=0, visitors=[], visits=[])
        rating_sum = 0
        for item in qs:
            stats['count']+=1
            rating_sum+=item.ratio
            stats['visitors'].append(UserSerializer(item.user).data)
            stats['visits'].append(VisitSerializer(item).data)
        if stats['count']>0:
            stats['avg']=rating_sum/stats['count']
        return stats



