from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import CommunityEvent
from rest_framework.decorators import action
from django.db.models import Count
from socioapi.models.communitymember import CommunityMember
from socioapi.models.member import Member
from django.db.models import Q
from django.core.files.base import ContentFile
import uuid
import base64


class CommunityEventView(ViewSet):

    @action(methods=["post"], detail=True)
    def attend(self, request, pk):
        member = Member.objects.get(user=request.auth.user)
        event = CommunityEvent.objects.get(pk=pk)
        event.attendees.add(member)
        return Response({'message': 'Your attending'}, status=status.HTTP_201_CREATED)

    @action(methods=["delete"], detail=True)
    def leave(self, request, pk):
        member = Member.objects.get(user=request.auth.user)
        event = CommunityEvent.objects.get(pk=pk)
        event.attendees.remove(member)
        return Response({'message': 'Not Attending'}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        try:
            member = Member.objects.get(user=request.auth.user)
            event = CommunityEvent.objects.annotate(
                attending_count=Count('attendingevent')).get(pk=pk)
            event.joined = member in event.attendees.all()
            serializer = CommunitySerializer(event)
            return Response(serializer.data)
        except CommunityEvent.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        filter = request.query_params.get('search', None)
        communitysearch = request.query_params.get('community', None)
        member = Member.objects.get(user=request.auth.user)
        event = CommunityEvent.objects.annotate(attending_count=Count('attendingevent')).filter(
            Q(public=True) |
            Q(community__members__member=member)
        )
        for events in event:
            events.joined = member in events.attendees.all()
        if filter is not None:
            event = event.filter(name__contains=filter)
        if communitysearch is not None:
            event = event.filter(community=communitysearch)
        serializer = CommunitySerializer(event, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        event = CommunityEvent.objects.get(pk=pk)
        serializer = CommunitySerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        member = Member.objects.get(user=request.auth.user)

        if request.data["image"] is not None:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                               name=f'{member.id}-{uuid.uuid4()}.{ext}')

        serializer = CreateCommunitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data["image"] is not None:
            serializer.save(image=data, member=member)
        else:
            serializer.save(member=member)
        return Response(serializer.data)

    def destroy(self, request, pk):
        event = CommunityEvent.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityEvent
        fields = ('id', 'name', 'date', 'address', 'approved', 'public', 'attendees', 'details', 'isactivity',
                  'zipcode', 'image', 'timestamp', 'community', 'member', 'time', "joined", 'attending_count')
        depth = 2


class CreateCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityEvent
        fields = fields = ("id",'name', 'date', 'address', 'approved', 'public', 'details', 'isactivity',
                  'zipcode', 'community', 'member', 'time')
