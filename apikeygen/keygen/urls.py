from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/get-key/', views.KeyView.as_view(), name='get_key'),  # Add parentheses here
    path('api/validate-key/', views.ValidateKeyView.as_view(), name='validate_key'),  # Add parentheses here
]
