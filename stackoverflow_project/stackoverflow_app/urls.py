from stackoverflow_app import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('search/', views.search),
]

urlpatterns = format_suffix_patterns(urlpatterns)