# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from todo.models import Todo
from todo.serializers import TodoSerializer, UserSerializer, TodoMetaSerializer

# Create your views here.


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id, 'obj': token})


class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserInfo(APIView):
	def get(self, request, format=None):
		owner = request.user
		todos = Todo.objects.filter(owner=owner, progress__lt=100).extra(select={
			'weighted':"(todo_todo.end - now()) * priority"}).order_by('weighted')
		todo_brief = todos[:6]
		user = User.objects.get(id=owner.id)
		name = user.username
		if len(user.first_name + user.last_name):
			name = ' '.join([user.first_name, user.last_name])
		return Response({
			'user': UserSerializer(user).data,
			'name': name,
			'todo_count': todos.count(),
			'todos': TodoMetaSerializer(todo_brief, many=True).data
		})



class TodoList(APIView):
	def get(self, request, format=None):
		owner = request.user
		obj = Todo.objects

		f = request.GET.get('filter')

		if f == u"all":
			obj = obj.filter(owner=owner)
		elif f == u"wip":
			obj = obj.filter(owner=owner, progress__lt = 100)
		elif f == u"done":
			obj = obj.filter(owner=owner, progress = 100)
		else:
			obj = obj.filter(owner=owner)


		o = request.GET.get('order')

		if o == u"priority":
			obj = obj.order_by('priority')
		elif o == u"weight":
			obj = obj.extra(select={'weight':"(todo_todo.end - now()) * priority"}).order_by('weight')
		elif o == u"progress":
			obj = obj.order_by('-progress')
		elif o == u"begin":
			obj = obj.order_by('begin')
		elif o == u"end":
			obj = obj.order_by('end')
		elif o == u"created":
			obj = obj.order_by('-created')
		elif o == u"modified":
			obj = obj.order_by('-modified')



		l = request.GET.get('limit')
		try:
			l = int(l)
		except:
			l = 10

		p = request.GET.get('page')
		try:
			p = int(p)
			if p < 0: p = 0
		except:
			p = 0
		
		count = obj.count()
		pages = (count + l - 1) / l
		obj = obj[p*l:p*l+l]

		serializer = TodoMetaSerializer(obj, many=True)
		return Response({
			'count': count,
			'page': p,
			'pages': pages,
			'data': serializer.data
		})

class TodoDetail(APIView):
	def get(self, request, pk, format=None):
		owner = request.user
		todo = get_object_or_404(Todo.objects.filter(owner=owner), pk=pk)
		serializer = TodoSerializer(todo)
		return Response(serializer.data)

class TodoAdd(APIView):
	def post(self, request, format=None):
		owner = request.user
		serializer_context = {'request': request, }
		serializer = TodoSerializer(data=request.data, context=serializer_context)
		if serializer.is_valid():
			serializer.save(owner=owner)
			return Response({'success': True})
		else:
			return Response({'success': False, 'details': serializer.errors})

class TodoEdit(APIView):
	def post(self, request, pk, format=None):
		owner = request.user
		todo = get_object_or_404(Todo.objects.filter(owner=owner), pk=pk)
		serializer = TodoSerializer(todo, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'success': True})
		else:
			return Response({'success': False, 'details': serializer.errors})

class TodoProgress(APIView):
	def get(self, request, pk, format=None):
		owner = request.user
		todo = get_object_or_404(Todo.objects.filter(owner=owner), pk=pk)
		p = request.GET.get('progress')
		try:
			p = int(p)
		except:
			p = 100
		todo.progress = p
		if todo.progress >= 0 and todo.progress <= 100:
			todo.save()
			return Response({'success': True})
		else:
			return Response({'success': False, 'details': "Progress Out Of Range"})

class TodoDelete(APIView):
	def get(self, request, pk, format=None):
		owner = request.user
		todo = get_object_or_404(Todo.objects.filter(owner=owner), pk=pk)
		todo.delete()
		return Response({'success': True})
