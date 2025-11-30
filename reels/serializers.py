from rest_framework import serializers
from django.conf import settings
from .models import ReelJob


class ReelJobSerializer(serializers.ModelSerializer):
    """Serializer for ReelJob model."""
    
    id = serializers.UUIDField(read_only=True)
    image_url = serializers.SerializerMethodField()
    audio_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ReelJob
        fields = [
            'id', 'status', 'tone', 'original_script', 'final_script',
            'image_url', 'audio_url', 'video_url',
            'created_at', 'updated_at', 'error_message'
        ]
        read_only_fields = [
            'id', 'status', 'final_script', 'image_url', 'audio_url',
            'video_url', 'created_at', 'updated_at', 'error_message'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            return f"{settings.BACKEND_BASE_URL}{obj.image.url}"
        return None
    
    def get_audio_url(self, obj):
        if obj.audio_file:
            return f"{settings.BACKEND_BASE_URL}{obj.audio_file.url}"
        return None
    
    def get_video_url(self, obj):
        if obj.video_file:
            return f"{settings.BACKEND_BASE_URL}{obj.video_file.url}"
        return None


class ReelJobListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing reels."""
    
    id = serializers.UUIDField(read_only=True)
    video_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ReelJob
        fields = [
            'id', 'status', 'tone', 'created_at', 'updated_at', 'video_url'
        ]
    
    def get_video_url(self, obj):
        if obj.video_file:
            return f"{settings.BACKEND_BASE_URL}{obj.video_file.url}"
        return None


class ReelJobCreateSerializer(serializers.Serializer):
    """Serializer for creating a new reel."""
    
    image = serializers.ImageField(required=True)
    script = serializers.CharField(required=True, max_length=10000)
    tone = serializers.ChoiceField(
        choices=['neutral', 'friendly', 'formal', 'energetic', 'dramatic'],
        default='neutral',
        required=False
    )
    use_rewrite = serializers.BooleanField(default=True, required=False)
    max_seconds = serializers.IntegerField(
        min_value=1,
        max_value=300,
        required=False,
        allow_null=True
    )

