from sqlite3 import Timestamp
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import Announcement
from django.db.models import Count
from django.db.models import Q
from django.core.files.base import ContentFile
import uuid
import base64

from socioapi.models.member import Member

class AnnouncementEventView(ViewSet):
    def retrieve(self,request,pk):
        try:
            announcement = Announcement.objects.annotate(comment_count=Count('thecomments')).get(pk=pk)
            serializer = AnnouncementSerializer(announcement)
            return Response(serializer.data)
        except Announcement.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        filter = request.query_params.get('search', None)
        communitysearch = request.query_params.get('community', None)
        member = Member.objects.get(user=request.auth.user)
        announcement = Announcement.objects.annotate(comment_count=Count('thecomments')).filter(
            Q(public=True) |
            Q(community__members__member=member)
        ).order_by('-timestamp')
        
        if filter is not None:
            announcement = announcement.filter(name__contains=filter)
        if communitysearch is not None:
            announcement = announcement.filter(community=communitysearch)
        serializer = AnnouncementSerializer(announcement, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        announcement = Announcement.objects.get(pk=pk)
        serializer = AnnouncementSerializer(announcement, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,request):
        member = Member.objects.get(user=request.auth.user)
        
        if request.data["image"] is not None:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{member.id}-{uuid.uuid4()}.{ext}')
            
        serializer = CreateAnnouncementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data["image"] is not None:
            serializer.save(image=data, member=member)
        else: 
            serializer.save(member=member)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        announcement = Announcement.objects.get(pk=pk)
        announcement.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('id', 'title', 'details', 'approved', 'public', 'zipcode', 'comments', 'image', 'timestamp', "community", 'member', 'comment_count')
        depth = 2
        
class CreateAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('title', 'details', 'approved', 'public', 'zipcode', 'comments',"community", 'member')