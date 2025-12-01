from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import ReelJob
from .serializers import (
    ReelJobSerializer,
    ReelJobListSerializer,
    ReelJobCreateSerializer
)
from .services.script_rewrite_service import rewrite_script, ScriptRewriteError
from .services.video_generation_runpod import generate_video_with_runpod_service
from .services.async_processor import process_video_async
from .services.audio_generation import generate_audio_for_approved_script


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class APIInfoView(APIView):
    """API information endpoint."""
    
    def get(self, request):
        return Response({
            'name': 'AI Reel Generator API',
            'version': '1.0.0',
            'endpoints': {
                'create_reel': 'POST /api/reels/',
                'rewrite_script': 'POST /api/reels/<id>/rewrite-script/',
                'approve_script': 'POST /api/reels/<id>/approve-script/',
                'regenerate_script': 'POST /api/reels/<id>/regenerate-script/',
                'generate_audio': 'POST /api/reels/<id>/generate-audio/',
                'generate_video': 'POST /api/reels/<id>/generate-video/',
                'list_reels': 'GET /api/reels/',
                'get_reel': 'GET /api/reels/<id>/',
                'delete_reel': 'DELETE /api/reels/<id>/',
            },
            'workflow': {
                'step1': 'POST /api/reels/ - Create reel with image and script',
                'step2': 'POST /api/reels/<id>/rewrite-script/ - Generate rewritten script (if use_rewrite=true)',
                'step3': 'POST /api/reels/<id>/approve-script/ - Approve script and generate video',
                'step4': 'GET /api/reels/<id>/ - Check status and get video URL',
                'alternative': 'POST /api/reels/<id>/regenerate-script/ - Regenerate script if not satisfied'
            }
        })


class ReelListView(APIView):
    """List and create reels."""
    
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        """
        List all reels with pagination and optional filtering.
        
        Query parameters:
        - status: Filter by status (pending, script_pending_approval, processing, done, error)
        - page: Page number (default: 1)
        - page_size: Items per page (default: 20)
        """
        queryset = ReelJob.objects.all().order_by('-created_at')
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Paginate results
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = ReelJobListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # Fallback if pagination is not used
        serializer = ReelJobListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new reel (Step 1).
        Only saves image and script, does NOT process yet.
        
        Required fields:
        - image: Image file
        - script: Script text
        
        Optional fields:
        - tone: neutral|friendly|formal|energetic|dramatic (default: neutral)
        - use_rewrite: true|false (default: true)
        - max_seconds: integer (optional)
        """
        # Validate input
        serializer = ReelJobCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        
        # Create ReelJob instance (status: pending)
        reel_job = ReelJob.objects.create(
            original_script=validated_data['script'],
            tone=validated_data.get('tone', 'neutral'),
            image=validated_data['image'],
        )
        
        # If use_rewrite is True, rewrite script immediately
        use_rewrite = validated_data.get('use_rewrite', True)
        if use_rewrite:
            try:
                rewritten_script = rewrite_script(
                    reel_job.original_script,
                    tone=validated_data.get('tone', 'neutral'),
                    max_seconds=validated_data.get('max_seconds')
                )
                reel_job.final_script = rewritten_script
                reel_job.status = 'script_pending_approval'
                reel_job.save()
            except ScriptRewriteError as e:
                reel_job.status = 'error'
                reel_job.error_message = str(e)
                reel_job.save()
        else:
            # No rewrite needed, use original script
            reel_job.final_script = reel_job.original_script
            reel_job.script_approved = True
            reel_job.status = 'script_approved'
            reel_job.save()
            
            # Generate audio immediately since script is auto-approved
            try:
                generate_audio_for_approved_script(reel_job)
                reel_job.refresh_from_db()
            except Exception as e:
                # Don't fail the request if audio generation fails
                # User can retry later
                pass
        
        # Return serialized response
        response_serializer = ReelJobSerializer(reel_job)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ReelDetailView(APIView):
    """Retrieve and delete a specific reel."""
    
    def get(self, request, pk):
        """
        Get detailed information about a specific reel.
        """
        reel_job = get_object_or_404(ReelJob, pk=pk)
        serializer = ReelJobSerializer(reel_job)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        """
        Delete a reel.
        """
        reel_job = get_object_or_404(ReelJob, pk=pk)
        reel_job.delete()
        return Response(
            {'message': 'Reel deleted successfully'},
            status=status.HTTP_200_OK
        )


class RewriteScriptView(APIView):
    """Rewrite script for a reel."""
    
    def post(self, request, pk):
        """
        Rewrite the script for a reel (Step 2).
        Generates a new rewritten version based on tone.
        
        Optional body parameters:
        - tone: neutral|friendly|formal|energetic|dramatic (default: uses reel's tone)
        - max_seconds: integer (optional)
        """
        reel_job = get_object_or_404(ReelJob, pk=pk)
        
        tone = request.data.get('tone', reel_job.tone)
        max_seconds = request.data.get('max_seconds')
        
        try:
            rewritten_script = rewrite_script(
                reel_job.original_script,
                tone=tone,
                max_seconds=max_seconds
            )
            
            reel_job.final_script = rewritten_script
            reel_job.tone = tone
            reel_job.status = 'script_pending_approval'
            reel_job.script_approved = False
            reel_job.save()
            
            serializer = ReelJobSerializer(reel_job)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ScriptRewriteError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ApproveScriptView(APIView):
    """Approve script and generate video."""
    
    def post(self, request, pk):
        """
        Approve the script and start video generation (Step 3).
        After approval, generates TTS audio and video using Runpod.
        
        Optional body parameters:
        - async: true|false (default: false) - Process in background
        """
        reel_job = get_object_or_404(ReelJob, pk=pk)
        
        if not reel_job.final_script:
            return Response(
                {'error': 'No script to approve. Please rewrite script first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Approve script
        reel_job.script_approved = True
        reel_job.status = 'script_approved'
        reel_job.save()
        
        # Generate audio first (user can preview before video generation)
        try:
            generate_audio_for_approved_script(reel_job)
            reel_job.refresh_from_db()
        except Exception as e:
            # If audio generation fails, still allow video generation
            # Audio will be generated during video generation
            pass
        
        # Check if async processing
        async_mode = (
            request.data.get('async', 'false').lower() == 'true' or
            settings.ASYNC_PROCESSING
        )
        
        if async_mode:
            # Process in background
            process_video_async(reel_job)
            
            serializer = ReelJobSerializer(reel_job)
            return Response({
                **serializer.data,
                'message': 'Script approved. Audio generated. Video generation started. Poll /api/reels/<id>/ for status.'
            }, status=status.HTTP_202_ACCEPTED)
        else:
            # Synchronous processing
            try:
                generate_video_with_runpod_service(reel_job)
                serializer = ReelJobSerializer(reel_job)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                reel_job.refresh_from_db()
                serializer = ReelJobSerializer(reel_job)
                return Response(
                    {
                        **serializer.data,
                        'error_message': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class RegenerateScriptView(APIView):
    """Regenerate script (user not satisfied, wants new version)."""
    
    def post(self, request, pk):
        """
        Regenerate the rewritten script (alternative to approve).
        User can call this multiple times until satisfied.
        
        Optional body parameters:
        - tone: neutral|friendly|formal|energetic|dramatic (default: uses reel's tone)
        - max_seconds: integer (optional)
        """
        reel_job = get_object_or_404(ReelJob, pk=pk)
        
        tone = request.data.get('tone', reel_job.tone)
        max_seconds = request.data.get('max_seconds')
        
        try:
            rewritten_script = rewrite_script(
                reel_job.original_script,
                tone=tone,
                max_seconds=max_seconds
            )
            
            reel_job.final_script = rewritten_script
            reel_job.tone = tone
            reel_job.status = 'script_pending_approval'
            reel_job.script_approved = False
            reel_job.save()
            
            serializer = ReelJobSerializer(reel_job)
            return Response({
                **serializer.data,
                'message': 'Script regenerated. Review and approve when ready.'
            }, status=status.HTTP_200_OK)
        
        except ScriptRewriteError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateAudioView(APIView):
    """Generate audio for an approved script (without video generation)."""
    
    def post(self, request, pk):
        """
        Generate TTS audio for a reel with approved script.
        Useful for previewing audio before video generation.
        
        Returns:
            Updated reel with audio_url
        """
        reel_job = get_object_or_404(ReelJob, pk=pk)
        
        if not reel_job.script_approved or not reel_job.final_script:
            return Response(
                {'error': 'Script must be approved before generating audio'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            generate_audio_for_approved_script(reel_job)
            reel_job.refresh_from_db()
            serializer = ReelJobSerializer(reel_job)
            return Response({
                **serializer.data,
                'message': 'Audio generated successfully. You can preview it before generating video.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            reel_job.refresh_from_db()
            serializer = ReelJobSerializer(reel_job)
            return Response(
                {
                    **serializer.data,
                    'error': f'Audio generation failed: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateVideoView(APIView):
    """Generate video for an approved script."""
    
    def post(self, request, pk):
        """
        Generate video for a reel with approved script.
        Can be called directly if script is already approved.
        
        Optional body parameters:
        - async: true|false (default: false)
        """
        reel_job = get_object_or_404(ReelJob, pk=pk)
        
        if not reel_job.script_approved or not reel_job.final_script:
            return Response(
                {'error': 'Script must be approved before generating video'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate audio if not already generated
        if not reel_job.audio_file:
            try:
                generate_audio_for_approved_script(reel_job)
                reel_job.refresh_from_db()
            except Exception as e:
                # Continue even if audio generation fails
                # It will be generated during video generation
                pass
        
        async_mode = (
            request.data.get('async', 'false').lower() == 'true' or
            settings.ASYNC_PROCESSING
        )
        
        if async_mode:
            process_video_async(reel_job)
            
            serializer = ReelJobSerializer(reel_job)
            return Response({
                **serializer.data,
                'message': 'Video generation started. Poll /api/reels/<id>/ for status.'
            }, status=status.HTTP_202_ACCEPTED)
        else:
            try:
                generate_video_with_runpod_service(reel_job)
                serializer = ReelJobSerializer(reel_job)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                reel_job.refresh_from_db()
                serializer = ReelJobSerializer(reel_job)
                return Response(
                    {
                        **serializer.data,
                        'error_message': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
