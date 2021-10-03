from rest_framework import serializers
from stackoverflow_app import models
from stackoverflow_app.request import Request


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Search
        fields = ['id', 'search_time', 'user_id', 'query']


class RequestSerializer(serializers.Serializer):
    intitle = serializers.CharField(max_length=50)
    nottagged = serializers.CharField(max_length=50)
    tagged = serializers.CharField(max_length=50)
    sort = serializers.CharField(max_length=10)
    order = serializers.CharField(max_length=10)
    todate = serializers.DateTimeField()
    fromdate = serializers.DateTimeField()
    pagesize = serializers.IntegerField(min_value=1, max_value=40)
    page = serializers.IntegerField(min_value=0)

    def create(self, data):
        return Request(data.get('intitle'), data.get('nottagged'), data.get('tagged'),
                       data.get('sort'), data.get('order'), data.get('todate'),
                       data.get('fromdate'), data.get('pagesize'), data.get('page'))