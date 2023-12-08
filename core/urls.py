from django.urls import path
from . import views

urlpatterns = [
    path('index/<int:conversation_id>/', views.index, name='index_with_id'),
    path('', views.index, name='index'),
    path('create-interjection/<int:conversation_id>/', views.create_interjection, name='create-interjection'),
    path('download-speech/<int:interjection_id>/', views.download_speech, name='download-speech'),
    path('play-speech/<int:interjection_id>/', views.play_speech, name='play-speech'),
    path('delete_conversation/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
    path('update_conversation/<int:conversation_id>/', views.update_conversation, name='update_conversation'),
    path('edit_conversation/<int:conversation_id>/', views.edit_conversation, name='edit_conversation'),
]
