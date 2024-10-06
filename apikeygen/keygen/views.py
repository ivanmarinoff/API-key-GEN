from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import APIKey


def index(request):
    """Landing page view to render a basic HTML page."""
    return render(request, 'index.html')  # Ensure 'index.html' exists in your templates directory


class KeyView(APIView):
    """View to handle GET requests for retrieving the latest active API key."""

    @staticmethod
    def get(request):
        # Remove expired keys before retrieving the latest one
        APIKey.objects.filter(expires_at__lt=timezone.now()).delete()

        # Retrieve the most recent valid key
        key_obj = APIKey.objects.filter(expires_at__gt=timezone.now()).order_by('-created_at').first()

        if key_obj:
            return Response({
                'key': key_obj.key,
                'expires_at': key_obj.expires_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return Response({'error': 'No valid key found'}, status=status.HTTP_404_NOT_FOUND)


class ValidateKeyView(APIView):
    """View to handle POST requests for validating API keys with a specific site URL."""

    @staticmethod
    def post(request):
        # Retrieve the key and site URL from the request data
        key = request.data.get('key')
        site_url = request.data.get('site_url')

        # Check if both key and site_url are provided
        if not key or not site_url:
            return Response({'error': 'Both "key" and "site_url" are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for the corresponding API key and site URL
        key_obj = get_object_or_404(APIKey, key=key, site_url=site_url)

        # Validate if the key is still valid for the given site
        if key_obj.expires_at > timezone.now():
            return Response({
                'detail': 'Key validated',
                'expires_at': key_obj.expires_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return Response({'detail': 'Key expired or invalid'}, status=status.HTTP_403_FORBIDDEN)

# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from django.shortcuts import render
# from django.utils import timezone
# from .models import APIKey
#
#
#
#
#
# def index(request):
#     return render(request, '../templates/index.html')
#
#
# class KeyView(APIView):
#     @staticmethod
#     def get(request):
#         # Remove expired keys before retrieving the latest one
#         APIKey.objects.filter(expires_at__lt=timezone.now()).delete()
#         current_key = APIKey.objects.filter(expires_at__gt=timezone.now()).order_by('-created_at').first()
#         if not current_key:
#             return Response({"detail": "No active key available"}, status=status.HTTP_404_NOT_FOUND)
#         return Response({"key": current_key.key})
#
#
# class ValidateKeyView(APIView):
#     @staticmethod
#     def post(request):
#         key = request.data.get('key')
#         if APIKey.objects.filter(key=key, expires_at__gt=timezone.now()).exists():
#             # Save the key in session with 24-hour expiration
#             request.session['api_key'] = key
#             request.session.set_expiry(86400)  # 24 hours in seconds
#             return Response({"detail": "Key validated"})
#         return Response({"detail": "Invalid or expired key"}, status=status.HTTP_401_UNAUTHORIZED)
