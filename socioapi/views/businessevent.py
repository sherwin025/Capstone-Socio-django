from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import BusinessEvent

class BusinessEventView(ViewSet):
    def retrieve(self,request,pk):
        try:
            businessEvent = BusinessEvent.objects.get(pk=pk)
            serializer = BusinessEventSerializer(businessEvent)
            return Response(serializer.data)
        except BusinessEvent.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        filter = request.query_params.get('search', None)
        businessEvent = BusinessEvent.objects.all()
        
        if filter is not None:
            businessEvent = businessEvent.filter(name__contains=filter)
        serializer = BusinessEventSerializer(businessEvent, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        businessEvent = BusinessEvent.objects.get(pk=pk)
        serializer = BusinessEventSerializer(businessEvent, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,request):
        serializer = CreateBusinessEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        businessEvent = BusinessEvent.objects.get(pk=pk)
        businessEvent.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class BusinessEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessEvent
        fields = "__all__"
        depth = 1
        
class CreateBusinessEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessEvent
        fields = "__all__"