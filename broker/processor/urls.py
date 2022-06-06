from django.urls import include, path
from .views import processor, create_userfield

urlpatterns = [
    path('', processor, name='processor'),
    path('create_userfield/', create_userfield, name='create_userfield'),
]