from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from core.models import Conversation, Interjection
from core.forms import ConversationForm 
from core.forms import HumanInterjectionForm, InterjectionForm
from django.http import JsonResponse
from .models import AudioRecording
import uuid
import os
import ffmpeg
from django.http import JsonResponse

from openai import OpenAI
import json  
from bs4 import BeautifulSoup
client = OpenAI()

from django.shortcuts import get_object_or_404

@login_required
def index(request, conversation_id=None):
    user = request.user
    
    if request.method == 'POST':
        form = ConversationForm(request.POST)
        if form.is_valid():
            conversation = form.save(commit=False)
            conversation.user = request.user
            conversation.save()
        else:
            redirect('index')
    else:
        # Fetch or create the conversation
        if conversation_id:
            # Get the specific conversation by ID, or return a 404 if it doesn't exist
            conversation = get_object_or_404(Conversation, id=conversation_id, user=user)
        else:
            # Get the latest conversation, or create a new one if none exists
            conversation = Conversation.objects.filter(user=user).order_by('-last_update').first()
            if not conversation:
                conversation = Conversation.objects.create(user=user, title="Initial Conversation")
        
        # Now conversation is either the specified one, the latest, or a new "Initial" conversation
    context = {
        'conversation': conversation,
        'conversations': Conversation.objects.filter(user=user).order_by('-last_update'),
        'conversation_form': ConversationForm(),
        'interjections': Interjection.objects.filter(conversation=conversation).order_by('-id'),
        'human_interjection_form': HumanInterjectionForm(),
    }
    return render(request, 'core/index.html', context)

def remove_html_markers(text):
    # Define the markers
    start_marker = "```html"
    end_marker = "```"
    
    # Check if the text starts with the start marker and remove it
    if text.startswith(start_marker):
        text = text[len(start_marker):]

    # Check if the text ends with the end marker and remove it
    if text.endswith(end_marker):
        text = text[:-len(end_marker)]

    return text

@login_required
@require_POST
def create_interjection(request, conversation_id=None):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    form = HumanInterjectionForm(request.POST)
    if form.is_valid():

        interjection = form.save(commit=False)

        language_id = interjection.language
        conversation_type_id = interjection.conversation_type
        audio = interjection.audio
        user_input = interjection.human

        language = 'French'
        if language_id == 'E': 
            language = 'English'
        elif language_id == 'S':
            language = 'Spanish'
        elif language_id == 'J':
            language = 'Japanese'
        elif language_id == 'G':
            language = 'German'
        elif language_id == 'I':
            language = 'Italian'



        response_format = { "type": "text" }
        model = "gpt-3.5-turbo-1106"

        prompt = (f"You are a proficient translator skilled in translating text from various languages to {language}. "
        "Your translations should be accurate, contextually appropriate, and sensitive to nuances in both the source and target languages. "
        "Format your translations using HTML, organizing them clearly in paragraphs or lists as needed. "
        "In cases of ambiguous phrases, provide the most likely translation or offer multiple interpretations. "
        "If a translation requires cultural or contextual explanation, include brief notes to clarify. "
        "Feel free to ask for clarification if any part of the text is unclear. Present your HTML-formatted translations.")
        if conversation_type_id == 'E':

            prompt = (f"You are a detail-oriented {language} language teacher specializing in text review. "
            "Examine texts in {language} for grammatical errors, typos, and areas needing improvement, including punctuation, sentence structure, and word choice. "
            "For each identified issue, provide a comprehensive explanation, including the nature of the mistake, its correction, and a rationale for the correction. "
            "Use HTML formatting to clearly distinguish between errors highlighted in red, corrections highlighted in yellow, and explanations (formatted as notes). "
            "Additionally, suggest improvements for enhancing clarity, style, and readability. "
            "If any part of the text is ambiguous, request clarification before proceeding. "
            "Present your feedback in an organized, HTML-formatted manner.")
        elif conversation_type_id == 'C':

            prompt = (f"You are a helpful individual, skilled in using {language} for engaging conversations. "
            "In your responses, adopt a friendly tone and informal style. "
            "Each reply should be thoughtful, reflecting understanding and interest in the conversation. "
            "Include a relevant follow-up question with each response to maintain engagement and deepen the dialogue. "
            "Use HTML formatting to enhance the presentation of your responses, utilizing bold or italics for emphasis and organizing content for easy readability. "
            "Be adaptable to various topics, ensuring that your responses and questions are always pertinent and engaging. "
            "Demonstrate active listening by tailoring your responses to the specifics of the conversation. "
            f"Remember to use {language} in all your communications.")
        

        response = client.chat.completions.create(
          model=model,
          response_format=response_format,
          messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
          ]

        )
        translate = response.choices[0].message.content
        translate = remove_html_markers(translate)

        #translate = json.loads(translate_json)
        print(translate)

        
        interjection.bot = translate
        interjection.conversation = conversation

        
        #response.stream_to_file("output.mp3")
        interjection.save()
        context = {'interjection' : interjection,
                   }
        conversation_id = conversation.id
        print(conversation_id)

        return render(request, f'core/index.html#interjection-partial', context)
    

@login_required
@require_http_methods(["GET"])
def play_speech(request, interjection_id=None):
    interjection = get_object_or_404(Interjection, id=interjection_id)
@login_required
@require_POST
def download_speech(request, interjection_id=None):
    interjection = get_object_or_404(Interjection, id=interjection_id)
    print(interjection.bot)
    soup = BeautifulSoup(interjection.bot, "lxml")

# Extract text
    text = soup.get_text()
    response = client.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            input=text,
    )
    
    # Generate a unique filename
    generated_uuid = str(uuid.uuid4())
    filename = '{}.aac'.format(generated_uuid)
    #filename_webm = '{}.webm'.format(generated_uuid)
    full_recordings_dir = os.path.join(settings.MEDIA_ROOT, 'recordings')
    recordings_dir = 'media/recordings'
    # Define the full path for the file
    file_path = os.path.join(recordings_dir, filename)
    file_path2 = os.path.join('recordings', filename)
    #file_path_webm = os.path.join('recordings', filename_webm)
    full_file_path = os.path.join(full_recordings_dir, filename)
    #full_file_path_webm = os.path.join(full_recordings_dir, filename_webm)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Stream the audio to the file
    response.stream_to_file(file_path)
    print(full_file_path)
    #print(full_file_path_webm)

    #ffmpeg.input(full_file_path).output(full_file_path_webm, vcodec='libvpx', acodec='libvorbis').run()

    # Update the Interjection instance
    interjection.bot_audio_file.name = file_path2
    interjection.audio = True
    interjection.save()
    print (interjection.bot_audio_file.url)
    partial = f'''
    <button onclick="playAudio('{interjection.bot_audio_file.url}')" class="text-xs opacity-80" title="Play Audio " hx-indicator="#loadingIndicator-{interjection.id}">

                                    <span class="material-symbols-outlined">
                                    play_circle
                                    </span>
                                </button>
    '''

    # Optionally, return a response
    return HttpResponse(partial)   



def upload_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio_file']
        recording = AudioRecording.objects.create(audio_file=audio_file)
        return JsonResponse({'status': 'success', 'audio_id': recording.id})
    return JsonResponse({'status': 'error'}, status=400)




def delete_conversation(request, conversation_id):
    # Your logic to delete the conversation
    Conversation.objects.filter(id=conversation_id).delete()
    return JsonResponse({'status': 'success'})


def update_conversation(request, conversation_id):
    # Your logic to update the conversation
    # e.g., update title
    new_title = request.POST.get('title')
    Conversation.objects.filter(id=conversation_id).update(title=new_title)
    conversation = Conversation.objects.get(id=conversation_id)
    context = {'conversation': conversation, 'conversation_id': conversation_id} 
    
    #return render(request, 'core/partials/conversation-partial.html', context ) 
    return render(request, 'core/index.html#conversation-partial', context ) 

def edit_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    form_edit_conversation = ConversationForm(instance=conversation)  # Assuming you have a form for editing
    context = {'form_edit_conversation': form_edit_conversation, 'conversation_id': conversation_id}
    return render(request, 'core/partials/edit_conversation.html', context )

