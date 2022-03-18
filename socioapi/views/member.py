from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import Member
from django.core.files.base import ContentFile
import uuid
import base64

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
        
        if request.data["image"] is not None:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{member.id}-{uuid.uuid4()}.{ext}')
    
        serializer = UpdateMemberSerializer(member, data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data["image"] is not None:
            serializer.save(image=data)
        else: 
            serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"
        depth = 1
        
class UpdateMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id", "details", "parent", "zipcode")
        depth = 1