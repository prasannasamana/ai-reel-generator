from django.urls import path
from .views import (
    APIInfoView,
    ReelListView,
    ReelDetailView
)

urlpatterns = [
    # API endpoints
    path('api/', APIInfoView.as_view(), name='api_info'),
    path('api/reels/', ReelListView.as_view(), name='api_reels'),
    path('api/reels/<uuid:pk>/', ReelDetailView.as_view(), name='api_reel_detail'),
]
