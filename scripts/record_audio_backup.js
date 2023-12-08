
// static/js/record_audio.js

document.addEventListener('DOMContentLoaded', function() {
    let mediaRecorder;
    let audioChunks = [];

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.getElementById("startRecord").addEventListener('click', function() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                // Check if the browser supports Opus in WebM, and set the mimeType accordingly
                const options = MediaRecorder.isTypeSupported('audio/webm; codecs=opus') 
                                ? { mimeType: 'audio/webm; codecs=opus' }
                                : { mimeType: 'audio/webm' }; // Fallback to WebM without Opus

                mediaRecorder = new MediaRecorder(stream, options);
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    document.getElementById("audioPlayback").src = audioUrl;
                    document.getElementById("playRecording").disabled = false; // Enable the play button
                    sendAudioToServer(audioBlob);
                };
                audioChunks = [];
                mediaRecorder.start();
                document.getElementById("stopRecord").disabled = false;
            });
    });

    document.getElementById("stopRecord").addEventListener('click', function() {
        mediaRecorder.stop();
        document.getElementById("stopRecord").disabled = true;
    });
    // Add event listener for the play button
    document.getElementById("playRecording").addEventListener('click', function() {
        const audioElement = document.getElementById("audioPlayback");
        if (audioElement) {
            audioElement.play(); // Play the audio
        }
    });

    function sendAudioToServer(audioBlob) {
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'recorded_audio.webm');
        formData.append('csrfmiddlewaretoken', csrftoken);

        fetch('/upload-audio/', {
            method: 'POST',
            body: formData
        }).then(response => response.json())
          .then(data => console.log(data))
          .catch(error => console.error(error));
    }

    function playAudio(audioUrl) {
        var audioPlayer = document.getElementById('botAudioPlayer');
        audioPlayer.src = audioUrl;
        audioPlayer.hidden = false; // Show the player
        audioPlayer.play(); // Start playback
    }
});
