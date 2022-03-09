from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import CommunityEvent

class CommunityEventView(ViewSet):
    def retrieve(self,request,pk):
        try:
            event = CommunityEvent.objects.get(pk=pk)
            serializer = CommunitySerializer(event)
            return Response(serializer.data)
        except CommunityEvent.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        filter = request.query_params.get('search', None)
        event = CommunityEvent.objects.all()
        
        if filter is not None:
            event = event.filter(name__contains=filter)
        serializer = CommunitySerializer(event, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        event = CommunityEvent.objects.get(pk=pk)
        serializer = CommunitySerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,request):
        serializer = CreateCommunitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        event = CommunityEvent.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityEvent
        fields = "__all__"
        depth = 1
        
class CreateCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityEvent
        fields = "__all__"