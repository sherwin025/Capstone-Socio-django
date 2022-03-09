from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import CommunityTag

class CommunityTagView(ViewSet):
    
    def list(self,request):
        filter = request.query_params.get('community', None)
        tag = CommunityTag.objects.all()
        
        if filter is not None:
            tag = tag.filter(community_id=filter)
        serializer = CommunityTagSerializer(tag, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = CreateCommunityTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        tag = CommunityTag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CommunityTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityTag
        fields = "__all__"
        depth = 1
        
class CreateCommunityTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityTag
        fields = "__all__"