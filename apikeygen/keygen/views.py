from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import APIKey
from django.utils import timezone
from rest_framework import status


def index(request):
    return render(request, '../templates/index.html')


class KeyView(APIView):
    @staticmethod
    def get(request):
        # Remove expired keys before retrieving the latest one
        APIKey.objects.filter(expires_at__lt=timezone.now()).delete()
        current_key = APIKey.objects.filter(expires_at__gt=timezone.now()).order_by('-created_at').first()
        if not current_key:
            return Response({"detail": "No active key available"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"key": current_key.key})


class ValidateKeyView(APIView):
    @staticmethod
    def post(request):
        key = request.data.get('key')
        if APIKey.objects.filter(key=key, expires_at__gt=timezone.now()).exists():
            # Save the key in session with 24-hour expiration
            request.session['api_key'] = key
            request.session.set_expiry(86400)  # 24 hours in seconds
            return Response({"detail": "Key validated"})
        return Response({"detail": "Invalid or expired key"}, status=status.HTTP_401_UNAUTHORIZED)
