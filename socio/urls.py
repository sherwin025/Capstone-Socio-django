from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from socioapi.views import MemberView, TagView,register_user, login_user, DirectMessageView, AnnouncementCommentView, MessageEventView, BusinessView,  CommunityEventView, BusinessEventView, AnnouncementEventView, CommunityMemberView, CommunityView, CommunityTagView
from django.conf.urls.static import static
from django.conf import settings

from socioapi.views.businessaccouncement import BusinessAnnouncementView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'members', MemberView, 'member')
router.register(r'tags', TagView, 'tag')
router.register(r'messages', DirectMessageView, 'message')
router.register(r'business', BusinessView, 'business')
router.register(r'businessevents', BusinessEventView, 'businessevent')
router.register(r'businessannouncements', BusinessAnnouncementView, 'businessannouncement')
router.register(r'communitytags', CommunityTagView, 'communitytag')
router.register(r'community', CommunityView, 'community')
router.register(r'communitymember', CommunityMemberView, 'communitymember')
router.register(r'events', CommunityEventView, 'communityevent')
router.register(r'announcements', AnnouncementEventView, 'communityannouncement')
router.register(r'messageboard', MessageEventView, 'communitymessage')
router.register(r'comments', AnnouncementCommentView, 'announcementcomment')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)