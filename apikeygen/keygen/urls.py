from django.urls import path
from .views import KeyView, ValidateKeyView, index

urlpatterns = [
    path('', index, name='index'),  # Home page for visualizing the keys
    path('get-key/', KeyView.as_view(), name='get_key'),
    path('validate-key/', ValidateKeyView.as_view(), name='validate_key'),
]
