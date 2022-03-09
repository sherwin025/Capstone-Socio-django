from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import CommunityMember

class CommunityMemberView(ViewSet):
    def retrieve(self,request,pk):
        try:
            communitymember = CommunityMember.objects.get(pk=pk)
            serializer = CommunityMemberSerializer(communitymember)
            return Response(serializer.data)
        except CommunityMember.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        community = CommunityMember.objects.all()
        serializer = CommunityMemberSerializer(community, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        community = CommunityMember.objects.get(pk=pk)
        serializer = CommunityMemberSerializer(community, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,request):
        serializer = CreateCommunityMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        community = CommunityMember.objects.get(pk=pk)
        community.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = "__all__"
        depth = 1
        
class CreateCommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = "__all__"