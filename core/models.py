from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass

class Todo(models.Model):
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class AudioRecording(models.Model):
    audio_file = models.FileField(upload_to='recordings/')


class Conversation(models.Model):
    title = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Interjection(models.Model):
    TYPE_TRANSLATE = 'T'
    TYPE_EDIT = 'E'
    TYPE_CHAT = 'C'

    TYPE_CHOICES = [
        (TYPE_TRANSLATE, 'Translate'),
        (TYPE_EDIT, 'Edit'),
        (TYPE_CHAT, 'Chat'),
    ]
    conversation_type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default=TYPE_TRANSLATE,
    )

    LANG_ENG = 'E'
    LANG_SPA = 'S'
    LANG_FRA = 'F'
    LANG_JAP = 'J'
    LANG_GER = 'G'
    LANG_ITA = 'I'

    LANG_CHOICES = [
        (LANG_ENG, 'English'),
        (LANG_SPA, 'Spanish'),
        (LANG_FRA, 'French'),
        (LANG_JAP, 'Japanese'),
        (LANG_GER, 'German'),
        (LANG_ITA, 'Italian'),
    ]
    language = models.CharField(
        max_length=1,
        choices=LANG_CHOICES,
        default=LANG_FRA,
        
    )
    human = models.TextField()
    bot = models.TextField()
    human_audio_file = models.FileField(upload_to='recordings/')
    bot_audio_file = models.FileField(upload_to='recordings/')
    audio = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
