from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.files.base import ContentFile
import uuid
import base64

from socioapi.models import Member


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)
    
    if authenticated_user is not None:
        member = Member.objects.get(user=authenticated_user)
            
        token = Token.objects.get(user=authenticated_user)
        data = {
            'member': member.id,
            'parent': member.parent,
            'token': token.key,
            'last_login': authenticated_user.last_login
        }
        
        authenticated_user.last_login = f'{timezone.now()}'
        authenticated_user.save()
        return Response(data)
    else:
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    
    if request.data["image"] is not None:
        format, imgstr = request.data["image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["username"]}-{uuid.uuid4()}.{ext}')
    
    
    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email'],
        is_staff=request.data['is_staff'],
        last_login=timezone.now()
    )
    
    if request.data["image"] is not None:
        member = Member.objects.create(
            details=request.data['details'],
            user=new_user,
            zipcode=request.data['zipcode'],
            parent=request.data['parent'],
            image=data
        )
    else:
        member = Member.objects.create(
            details=request.data['details'],
            user=new_user,
            zipcode=request.data['zipcode'],
            parent=request.data['parent']
        )

    token = Token.objects.create(user=member.user)
    
    data = {
        'token': token.key,
        'member': member.id,
        'parent': member.parent
        }
    
    return Response(data)
