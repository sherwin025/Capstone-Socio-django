from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import MessageBoard

class MessageEventView(ViewSet):
    def retrieve(self,request,pk):
        try:
            message = MessageBoard.objects.get(pk=pk)
            serializer = MessageBoardSerializer(message)
            return Response(serializer.data)
        except MessageBoard.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        filter = request.query_params.get('search', None)
        communitysearch = request.query_params.get('community', None)
        message = MessageBoard.objects.all()
        
        if filter is not None:
            message = message.filter(name__contains=filter)
        if communitysearch is not None:
            message = message.filter(community=communitysearch)
        serializer = MessageBoardSerializer(message, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        message = MessageBoard.objects.get(pk=pk)
        serializer = MessageBoardSerializer(message, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,request):
        serializer = CreateMessageBoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        message = MessageBoard.objects.get(pk=pk)
        message.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class MessageBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageBoard
        fields = "__all__"
        depth = 2    
        
class CreateMessageBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageBoard
        fields = "__all__"