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
from .services.reel_pipeline import process_reel_job


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
                'list_reels': 'GET /api/reels/',
                'get_reel': 'GET /api/reels/<id>/',
                'delete_reel': 'DELETE /api/reels/<id>/',
            },
            'documentation': {
                'create_reel': {
                    'method': 'POST',
                    'url': '/api/reels/',
                    'content_type': 'multipart/form-data',
                    'required_fields': ['image', 'script'],
                    'optional_fields': {
                        'tone': 'neutral|friendly|formal|energetic|dramatic (default: neutral)',
                        'use_rewrite': 'true|false (default: true)',
                        'max_seconds': 'integer (optional)'
                    },
                    'response': {
                        'id': 'UUID',
                        'status': 'pending|processing|done|error',
                        'video_url': 'URL to video file (when done)',
                        'error_message': 'Error message (if error)'
                    }
                },
                'list_reels': {
                    'method': 'GET',
                    'url': '/api/reels/',
                    'query_params': {
                        'status': 'Filter by status (optional)',
                        'page': 'Page number (default: 1)',
                        'page_size': 'Items per page (default: 20)'
                    }
                },
                'get_reel': {
                    'method': 'GET',
                    'url': '/api/reels/<id>/',
                    'response': 'Full reel details including all URLs'
                },
                'delete_reel': {
                    'method': 'DELETE',
                    'url': '/api/reels/<id>/'
                }
            }
        })


class ReelListView(APIView):
    """List and create reels."""
    
    def get(self, request):
        """
        List all reels with pagination and optional filtering.
        
        Query parameters:
        - status: Filter by status (pending, processing, done, error)
        - page: Page number (default: 1)
        - page_size: Items per page (default: 20)
        """
        queryset = ReelJob.objects.all().order_by('-created_at')
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Paginate results
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        
        if page is not None:
            serializer = ReelJobListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # Fallback if pagination is not used
        serializer = ReelJobListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new reel.
        
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
        
        # Create ReelJob instance
        reel_job = ReelJob.objects.create(
            original_script=validated_data['script'],
            tone=validated_data.get('tone', 'neutral'),
            image=validated_data['image'],
        )
        
        # Process the reel job
        try:
            process_reel_job(
                reel_job=reel_job,
                use_rewrite=validated_data.get('use_rewrite', True),
                tone=validated_data.get('tone', 'neutral'),
                max_seconds=validated_data.get('max_seconds')
            )
            
            # Return serialized response
            response_serializer = ReelJobSerializer(reel_job)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            # Refresh from database to get updated error_message
            reel_job.refresh_from_db()
            response_serializer = ReelJobSerializer(reel_job)
            return Response(
                {
                    **response_serializer.data,
                    'error_message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
