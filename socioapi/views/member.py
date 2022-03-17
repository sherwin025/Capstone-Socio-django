from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import Member

class MemberView(ViewSet):
    def retrieve(self,request,pk):
        try:
            member = Member.objects.get(pk=pk)
            serializer = MemberSerializer(member)
            return Response(serializer.data)
        except Member.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        member = Member.objects.all()
        serializer = MemberSerializer(member, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        member = Member.objects.get(pk=pk)
        serializer = MemberSerializer(member, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"
        depth = 1