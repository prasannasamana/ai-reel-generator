"""
Runpod Serverless Handler for Django API
This wraps Django to work with Runpod Serverless endpoints
"""
import os
import sys
import json
from io import BytesIO
from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reel_platform.settings')
django_app = get_wsgi_application()


def handler(event):
    """
    Runpod Serverless handler function.
    
    Args:
        event: Dictionary containing:
            - method: HTTP method (GET, POST, etc.)
            - path: Request path
            - headers: HTTP headers
            - body: Request body (string or dict)
            - query: Query parameters (dict)
    
    Returns:
        Dictionary with:
            - statusCode: HTTP status code
            - headers: Response headers
            - body: Response body (string)
    """
    try:
        # Parse event
        method = event.get('method', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        body = event.get('body', '')
        query_params = event.get('query', {})
        
        # Convert body to bytes if it's a string
        if isinstance(body, str):
            body_bytes = body.encode('utf-8')
        elif isinstance(body, dict):
            body_bytes = json.dumps(body).encode('utf-8')
        else:
            body_bytes = body if isinstance(body, bytes) else b''
        
        # Create WSGI environment
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': '&'.join([f'{k}={v}' for k, v in query_params.items()]),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '8000',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': BytesIO(body_bytes),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }
        
        # Add headers to environ
        for key, value in headers.items():
            key = key.upper().replace('-', '_')
            if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                key = f'HTTP_{key}'
            environ[key] = value
        
        # Set content length
        environ['CONTENT_LENGTH'] = str(len(body_bytes))
        
        # Create WSGI request and get response
        request = WSGIRequest(environ)
        response = django_app(request)
        
        # Convert Django response to Runpod format
        response_body = b''.join(response).decode('utf-8')
        
        return {
            'statusCode': response.status_code,
            'headers': dict(response.items()),
            'body': response_body
        }
    
    except Exception as e:
        import traceback
        error_msg = {
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(error_msg)
        }

