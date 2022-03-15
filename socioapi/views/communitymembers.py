from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import CommunityMember
from socioapi.models.member import Member

class CommunityMemberView(ViewSet):
    def retrieve(self,request,pk):
        try:
            communitymember = CommunityMember.objects.get(pk=pk)
            serializer = CommunityMemberSerializer(communitymember)
            return Response(serializer.data)
        except CommunityMember.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        filter = request.query_params.get('member', None)
        filter2 = request.query_params.get('community', None)
        community = CommunityMember.objects.all()
        if filter is not None:
            community = community.filter(member=filter, community=filter2)
        if filter2 is not None:
            community = community.filter(community=filter2)
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
        depth = 2
        
class CreateCommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = "__all__"