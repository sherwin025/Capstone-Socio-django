from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import Business

class BusinessView(ViewSet):
    def retrieve(self,request,pk):
        try:
            business = Business.objects.get(pk=pk)
            serializer = BusinessSerializer(business)
            return Response(serializer.data)
        except Business.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        filter = request.query_params.get('search', None)
        business = Business.objects.all()
        
        if filter is not None:
            business = business.filter(name__contains=filter)
        serializer = BusinessSerializer(business, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        business = Business.objects.get(pk=pk)
        serializer = BusinessSerializer(business, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,request):
        serializer = BusinessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        business = Business.objects.get(pk=pk)
        business.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"