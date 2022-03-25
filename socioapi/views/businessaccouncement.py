from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from socioapi.models import BusinessAnnouncement

class BusinessAnnouncementView(ViewSet):
    def retrieve(self,request,pk):
        try:
            businessAnnouncement = BusinessAnnouncement.objects.get(pk=pk)
            serializer = BusinessAnnouncementSerializer(businessAnnouncement)
            return Response(serializer.data)
        except BusinessAnnouncement.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self,request):
        filter = request.query_params.get('search', None)
        businessAnnouncement = BusinessAnnouncement.objects.all().order_by('-timestamp')
        
        if filter is not None:
            businessAnnouncement = businessAnnouncement.filter(name__contains=filter)
        serializer = BusinessAnnouncementSerializer(businessAnnouncement, many=True)
        return Response(serializer.data)
    
    def update(self, request,pk):
        businessAnnouncement = BusinessAnnouncement.objects.get(pk=pk)
        serializer = BusinessAnnouncementSerializer(businessAnnouncement, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def create(self,request):
        serializer = CreateBusinessAnnouncementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        businessAnnouncement = BusinessAnnouncement.objects.get(pk=pk)
        businessAnnouncement.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class BusinessAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAnnouncement
        fields = "__all__"
        depth = 1
         
class CreateBusinessAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAnnouncement
        fields = "__all__"