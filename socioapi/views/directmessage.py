from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import DirectMessage, Member
from django.db.models import Q
from django.core.files.base import ContentFile
import uuid
import base64

class DirectMessageView(ViewSet):
    def retrieve(self,request,pk):
        try:
            directMessage = DirectMessage.objects.get(pk=pk)
            serializer = DirectMessageSerializer(directMessage)
            return Response(serializer.data)
        except DirectMessage.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        member = Member.objects.get(user=request.auth.user)
        directMessage = DirectMessage.objects.all()
        directMessage = directMessage.filter(Q(recipient=member) | Q(sender=member))
        serializer = DirectMessageSerializer(directMessage, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        member = Member.objects.get(user=request.auth.user)
        
        if request.data["image"] is not None:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{member.id}-{uuid.uuid4()}.{ext}')
        
        serializer = CreateDirectMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data["image"] is not None:
            serializer.save(image=data)
        else: 
            serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        directMessage = DirectMessage.objects.get(pk=pk)
        directMessage.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class DirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = "__all__"
        depth = 2
        
class CreateDirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ("content", "read", "recipient", "sender", "title")