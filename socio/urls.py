from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from socioapi.views import MemberView, TagView,register_user, login_user, DirectMessageView, BusinessView, CommunityEventView, BusinessEventView, CommunityMemberView, CommunityView, CommunityTagView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'members', MemberView, 'member')
router.register(r'tags', TagView, 'tag')
router.register(r'messages', DirectMessageView, 'message')
router.register(r'business', BusinessView, 'business')
router.register(r'businessevents', BusinessEventView, 'businessevent')
router.register(r'communitytags', CommunityTagView, 'communitytag')
router.register(r'communities', CommunityView, 'community')
router.register(r'communitymember', CommunityMemberView, 'communitymember')
router.register(r'events', CommunityEventView, 'communityevent')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]