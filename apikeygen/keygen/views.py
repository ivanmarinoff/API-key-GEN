# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import APIKey
# from django.utils import timezone
# from rest_framework import status


from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import APIKey
import json


def index(request):
    """Landing page view to render a basic HTML page."""
    return render(request, 'index.html')  # Make sure 'index.html' exists in your templates directory


class KeyView(View):
    """View to handle GET requests for retrieving API keys based on the site URL."""

    def get(self, request, *args, **kwargs):
        # Assume the site URL is passed as a GET parameter
        site_url = request.GET.get('site_url')
        if not site_url:
            return JsonResponse({'error': 'site_url parameter is missing'}, status=400)

        # Look up the key for the given site
        key_obj = get_object_or_404(APIKey, site_url=site_url)

        # Check if the key is still valid
        if key_obj.expires_at > timezone.now():
            return JsonResponse({
                'key': key_obj.key,
                'expires_at': key_obj.expires_at.strftime('%Y-%m-%d %H:%M:%S')  # Include expiration date in response
            })
        else:
            return JsonResponse({'error': 'Key expired'}, status=403)


class ValidateKeyView(View):
    """View to handle POST requests for validating API keys with a specific site URL."""

    def post(self, request, *args, **kwargs):
        # Parse the request body to get the key and site URL
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

        key = data.get('key')
        site_url = data.get('site_url')

        # Check if both key and site_url are provided
        if not key or not site_url:
            return JsonResponse({'error': 'Both "key" and "site_url" are required'}, status=400)

        # Check for the corresponding API key and site URL
        key_obj = get_object_or_404(APIKey, key=key, site_url=site_url)

        # Validate if the key is still valid for the given site
        if key_obj.expires_at > timezone.now():
            return JsonResponse({
                'detail': 'Key validated',
                'expires_at': key_obj.expires_at.strftime('%Y-%m-%d %H:%M:%S')  # Include expiration date in response
            })
        else:
            return JsonResponse({'detail': 'Key expired or invalid'}, status=403)


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
