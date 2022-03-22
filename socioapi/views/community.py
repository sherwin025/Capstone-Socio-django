
from sqlite3 import Timestamp
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import Community
from socioapi.models.communitymember import CommunityMember
from socioapi.models.member import Member
from django.db.models import Count
from rest_framework.decorators import action
from django.db.models import Q
from django.core.files.base import ContentFile
import uuid
import base64


class CommunityView(ViewSet):
    
    
    def retrieve(self,request,pk):
        member = Member.objects.get(user=request.auth.user)
        try:
            community = Community.objects.annotate(member_count=Count('members', filter=Q(members__approved=True), distinct=True), event_count=Count('events', distinct=True), announcement_count=Count('announcements', distinct=True)).get(pk=pk)
            try:
                object = CommunityMember.objects.get(community=community, member=member)
                community.joined = object is not None
            except CommunityMember.DoesNotExist as ex:
                community.joined = False
            serializer = CommunitySerializer(community)
            return Response(serializer.data)
        except Community.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self,request):
        membercommunties = request.query_params.get('member', None)
        filter = request.query_params.get('search', None)
        member = Member.objects.get(user=request.auth.user)
        community = Community.objects.annotate(member_count=Count('members', distinct=True), event_count=Count('events', distinct=True), announcement_count=Count('announcements', distinct=True)).filter(
            Q(public=True) |
            Q(members__member=member)
        )
        for comm in community:
            try: 
                object = CommunityMember.objects.get(community=comm, member=member)
                comm.joined = object is not None
            except CommunityMember.DoesNotExist as ex:
                comm.joined = False
        if filter is not None:
            community = community.filter(
                Q(name__contains=filter) |
                Q(about__contains=filter) |
                Q(tags__label__contains=filter)
                )
        if membercommunties is not None:
            community = community.filter(members__member=member, members__approved=True)

        serializer = CommunitySerializer(community, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        community = Community.objects.get(pk=pk)
        serializer = CommunitySerializer(community, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,request):
        member = Member.objects.get(user=request.auth.user)
        
        if request.data["image"] is not None:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{member.id}-{uuid.uuid4()}.{ext}')
            
        serializer = CreateCommunitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data["image"] is not None:
            serializer.save(image=data, createdby=member)
        else: 
            serializer.save(createdby=member)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        community = Community.objects.get(pk=pk)
        community.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ("id", 'name', 'public', 'visible', 'about', 'parentportal', 'rules', 'createdby', 'image', 'timestamp', 'joined', "member_count", 'event_count', "announcement_count", "members")
        depth = 1
        
class CreateCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ('id', 'name', 'public', 'visible', 'about', 'parentportal', 'rules')