# from django.http import JsonResponse
# from django.views import View
# from django.shortcuts import render, get_object_or_404
# from django.utils import timezone
# from .models import APIKey
# import json
#
#
# def index(request):
#     """Landing page view to render a basic HTML page."""
#     return render(request, 'index.html')  # Ensure 'index.html' exists in your templates directory
#
#
# class KeyView(View):
#     """View to handle GET requests for retrieving API keys based on the site URL."""
#
#     def get(self, request, *args, **kwargs):
#         # Assume the site URL is passed as a GET parameter
#         site_url = request.GET.get('site_url')
#         if not site_url:
#             return JsonResponse({'error': 'site_url parameter is missing'}, status=400)
#
#         # Look up the key for the given site URL
#         key_obj = APIKey.objects.filter(site_url=site_url, expires_at__gt=timezone.now()).first()
#
#         if key_obj:
#             # If the key is found and still valid, return it
#             return JsonResponse({
#                 'key': key_obj.key,
#                 'expires_at': key_obj.expires_at.strftime('%Y-%m-%d %H:%M:%S')
#             })
#         else:
#             # Return 404 if no valid key is found
#             return JsonResponse({'error': 'No valid key found for the given site URL'}, status=404)
#
#
# class ValidateKeyView(View):
#     """View to handle POST requests for validating API keys with a specific site URL."""
#
#     def post(self, request, *args, **kwargs):
#         # Parse the request body to get the key and site URL
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
#
#         key = data.get('key')
#         site_url = data.get('site_url')
#
#         # Check if both key and site_url are provided
#         if not key or not site_url:
#             return JsonResponse({'error': 'Both "key" and "site_url" are required'}, status=400)
#
#         # Check for the corresponding API key and site URL
#         key_obj = get_object_or_404(APIKey, key=key, site_url=site_url)
#
#         # Validate if the key is still valid for the given site
#         if key_obj.expires_at > timezone.now():
#             return JsonResponse({
#                 'detail': 'Key validated',
#                 'expires_at': key_obj.expires_at.strftime('%Y-%m-%d %H:%M:%S')
#             })
#         else:
#             return JsonResponse({'detail': 'Key expired or invalid'}, status=403)
