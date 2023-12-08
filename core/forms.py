from django import forms
from core.models import Todo
from core.models import Conversation
from core.models import Interjection


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['description', 'is_completed']

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation 
        fields = ['title'] 

class HumanInterjectionForm(forms.ModelForm):
    conversation_type = forms.ChoiceField(
        choices=Interjection.TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial=Interjection.TYPE_CHAT
    )
    class Meta:
        model = Interjection 
        fields = ['human', 'language', 'conversation_type']


class InterjectionForm(forms.ModelForm):
    class Meta:
        model = Interjection 
        fields = ['human', 'bot']


