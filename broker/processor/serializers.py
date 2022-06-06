from rest_framework import serializers
from .models import Application

class ClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    phone = serializers.IntegerField()
    adress = serializers.CharField(max_length=200)

class DealSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=200)
    client = ClientSerializer()
    products = serializers.ListField()
    delivery_adress = serializers.CharField(max_length=200)
    delivery_date = serializers.DateTimeField()
    delivery_code = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Application(**validated_data)


