# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView



class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        name = user.username
        if len(user.first_name + user.last_name):
        	name = ' '.join([user.first_name, user.last_name])
        return Response({
        	'token': token.key, 
        	'id': token.user_id, 
        	'user': {
        		'username': user.username,
        		'email': user.email,
        		'name': name,
        	}})


@authentication_classes([])
@permission_classes([])
class UserCreate(APIView):
    def post(self, request, format=None):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        try:
            user.save()
            return Response({'success': True})
        except Exception, e:
            return Response({'success': False, 'detail': str(e)})

