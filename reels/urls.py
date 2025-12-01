from django.urls import path
from .views import (
    APIInfoView,
    ReelListView,
    ReelDetailView,
    RewriteScriptView,
    ApproveScriptView,
    RegenerateScriptView,
    GenerateAudioView,
    GenerateVideoView
)

urlpatterns = [
    # API endpoints
    path('api/', APIInfoView.as_view(), name='api_info'),
    path('api/reels/', ReelListView.as_view(), name='api_reels'),
    path('api/reels/<uuid:pk>/', ReelDetailView.as_view(), name='api_reel_detail'),
    path('api/reels/<uuid:pk>/rewrite-script/', RewriteScriptView.as_view(), name='rewrite_script'),
    path('api/reels/<uuid:pk>/approve-script/', ApproveScriptView.as_view(), name='approve_script'),
    path('api/reels/<uuid:pk>/regenerate-script/', RegenerateScriptView.as_view(), name='regenerate_script'),
    path('api/reels/<uuid:pk>/generate-audio/', GenerateAudioView.as_view(), name='generate_audio'),
    path('api/reels/<uuid:pk>/generate-video/', GenerateVideoView.as_view(), name='generate_video'),
]
