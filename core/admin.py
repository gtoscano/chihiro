from django.contrib import admin
from core.models import Todo, AudioRecording
from core.models import Conversation
from core.models import Interjection

class TodoAdmin(admin.ModelAdmin):
    pass
class AudioRecordingAdmin(admin.ModelAdmin):
    pass
class ConversationAdmin(admin.ModelAdmin):
    pass
class InterjectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Todo, TodoAdmin)
admin.site.register(AudioRecording, AudioRecordingAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Interjection, InterjectionAdmin)
