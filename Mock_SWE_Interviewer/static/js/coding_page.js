document.addEventListener("DOMContentLoaded", function () {
    let editor = null;
    /// For visual studio code editor
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.21.2/min/vs' }});
    require(['vs/editor/editor.main'], function() {
        editor = monaco.editor.create(document.getElementById('editor'), {
            value: '',
            language: 'python',
            theme: 'vs-dark'
        });
    });
    /// Gets the text from the texteditor 
    document.getElementById('submit_code').addEventListener('click', function() {
        var code = editor.getValue();
        console.log(code);
    });

    // Speech reconition
    // Check if browser supports Web Speech API
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = true; // Keep listening even after pauses
        recognition.interimResults = true; // Show interim results before finalizing
        recognition.lang = 'en-US'; // Set language
    }
    recognition.onresult = (event) => {
        window.transcriptText = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            window.transcriptText += event.results[i][0].transcript + ' ';
        } // need to send it to python backend
        console.log(window.transcriptText); // console is successfully logging the transcript
    }

    /// Gets each chunk of the question and displays it on the page slowly. Acts like chatgpt texting style
    var total_questions = '' 
    var total_format = ''
    var generated_question = false 
    if (!generated_question){
        var question_source = new EventSource('/question');
        question_source.onmessage = function(event) { 
            total_questions += event.data; 
            document.getElementById('question').innerHTML = total_questions;
        };
    }
    question_source.addEventListener('end', function(event){
        question_source.close(); 
        total_questions = '';
        generated_question = true;
        var format_source = new EventSource('/format');

        format_source.onmessage = function(event) {
            // in progress 
            total_format += event.data;
            total_format = total_format.split('\\n').join('\n')
            editor.setValue(total_format);
        };

        format_source.addEventListener('end', function(event){
            total_format = '';
            format_source.close();
        })
    })

    // gets mic input and mic process
    const micOverlay = document.getElementById("micOverlay");
    const micButton = document.getElementById("micButton");
    let isListening = false;
    let audioContext = null;
    let analyser = null;

    // Get the mic input and start the mic
    async function get_mic(){
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        micButton.style.display = 'block';
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        var source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);
        analyser.fftSize = 256;
        const dataArray = new Uint8Array(analyser.frequencyBinCount);
        window.analyser = analyser;
        window.dataArray = dataArray;
    }
    get_mic(); // starts it immediately

    // for overlaying on the micorphone image
    let intensity = 0.5; // Default intensity value
    let request_animation_frame = null; 

    // starts recognition and overlay when button is pressed 
    function start_overlay() {
        recognition.start();
        micOverlay.style.backgroundColor = `rgba(255, 0, 0, ${intensity})`; // Adjust red tint transparency
    }
    // continously updates the overlay as mic gets loduer
    function update_overlay() {
        window.analyser.getByteFrequencyData(window.dataArray);
        const micLevel = Math.max(...window.dataArray); // Get the max volume level
        intensity = Math.min(1, micLevel / 128); // Scale intensity (0 to 1)
        micOverlay.style.backgroundColor = `rgba(255, 0, 0, ${intensity})`; // Adjust red tint transparency
        request_animation_frame = requestAnimationFrame(update_overlay); // recursive calls itself
    }
    // stops the recognition and removes the overlay
    function removeOverlay() {
        recognition.stop();
        micOverlay.style.backgroundColor = "rgba(255, 0, 0, 0)";
    }
    // every time the button is clicked, either it will remove overlay or add overlays
    micButton.addEventListener("click", () => {
        if (isListening) {
            cancelAnimationFrame(request_animation_frame)
            request_animation_frame = null;
            removeOverlay();
            isListening = false;
            
            // Sending the voice transcript to python 
            fetch('http://127.0.0.1:5000/speech_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(window.transcriptText) 
            })
                .then(response => response.json())
                .then(data => {
                    // clear all audio setting from microphone which was previously used
                    audioContext = new (window.AudioContext || window.webkitAudioContext)(); 
                    analyser = audioContext.createAnalyser();
                    analyser.fftSize = 1024;

                    console.log('Response received from Flask | /speech_data') // Log
                    const audio = new Audio(`/static/audio_data/output.wav?timestamp=${new Date().getTime()}`);
                    const source = audioContext.createMediaElementSource(audio);
                    source.connect(analyser);
                    analyser.connect(audioContext.destination);
                    audio.play(); // play audio 
                })
        } else {
            start_overlay();
            request_animation_frame = requestAnimationFrame(update_overlay); // Start updating the overlay
            isListening = true;
        }
    })        

    // get user code and sends it to python when requested 
    fetch('http://127.0.0.1:5000/get_user_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(editor.getValue())
    })
        .then(response => response.json())

});



