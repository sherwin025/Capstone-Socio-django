from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import DirectMessage

class DirectMessageView(ViewSet):
    def retrieve(self,request,pk):
        try:
            directMessage = DirectMessage.objects.get(pk=pk)
            serializer = DirectMessageSerializer(directMessage)
            return Response(serializer.data)
        except DirectMessage.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        directMessage = DirectMessage.objects.all()
        serializer = DirectMessageSerializer(directMessage, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = CreateDirectMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
        depth = 1
        
class CreateDirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = "__all__"