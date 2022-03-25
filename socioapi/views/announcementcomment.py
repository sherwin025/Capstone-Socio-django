from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import AnnouncementComment

class AnnouncementCommentView(ViewSet):
    def retrieve(self,request,pk):
        try:
            comment = AnnouncementComment.objects.get(pk=pk)
            serializer = AnnouncementCommentSerializer(comment)
            return Response(serializer.data)
        except AnnouncementComment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        filter = request.query_params.get('search', None)
        comment = AnnouncementComment.objects.all().order_by('-timestamp')
        
        if filter is not None:
            comment = comment.filter(name__contains=filter)
        serializer = AnnouncementCommentSerializer(comment, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        comment = AnnouncementComment.objects.get(pk=pk)
        serializer = AnnouncementCommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,request):
        serializer = CreateAnnouncementCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        comment = AnnouncementComment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class AnnouncementCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementComment
        fields = "__all__"
        depth = 2
        
class CreateAnnouncementCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementComment
        fields = "__all__"