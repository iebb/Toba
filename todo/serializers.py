# coding=utf-8

from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import User
from rest_framework import serializers
from todo.models import Todo
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    todo = serializers.PrimaryKeyRelatedField(many=True, queryset=Todo.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'todo', 'first_name', 'last_name', 'email')

class TodoMetaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    weight = serializers.SerializerMethodField()
    def get_weight(self, obj):
        return (obj.end - timezone.now()) * obj.priority
    class Meta:
        model = Todo
        fields = ('id', 'created', 'modified', 'begin', 'end', 'title', 'description', 'progress', 'priority', 'owner', 'weight')

class TodoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    weight = serializers.SerializerMethodField()
    def get_weight(self, obj):
        return (obj.end - timezone.now()) * obj.priority
    def validate(self, data):
        if data['begin'] > data['end']:
            raise serializers.ValidationError("Start date should be earlier than end date")
        elif data['priority'] < 1 or data['priority'] > 1000:
            raise serializers.ValidationError("Priority should be an integer between 1 and 1000")
        elif data['progress'] < 1 or data['progress'] > 100:
            raise serializers.ValidationError("Progress should be an integer between 1 and 100")
        else:
            return data
    class Meta:
        model = Todo
        fields = ('id', 'created', 'modified', 'begin', 'end', 'title', 'description', 'progress', 'priority', 'owner', 'markdown', 'weight')
