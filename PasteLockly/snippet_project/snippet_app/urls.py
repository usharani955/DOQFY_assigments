from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_snippet, name='create_snippet'),
    path('snippet/<int:snippet_id>/', views.view_snippet, name='view_snippet'),
]

