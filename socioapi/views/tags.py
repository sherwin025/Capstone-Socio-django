from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import Tag

class TagView(ViewSet):
    def retrieve(self,request,pk):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        filter = request.query_params.get('search', None)
        tag = Tag.objects.all()
        
        if filter is not None:
            tag = tag.filter(label__contains=filter)
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        tag = Tag.objects.get(pk=pk)
        tag.label = request.data['label']
        tag.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,request):
        tag = Tag.objects.create(
            label=request.data['label']
        )
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"