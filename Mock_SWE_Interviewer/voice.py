from google.cloud import texttospeech
import os
import wave

# Initializes text to speech client with the voice using google cloud text to speech 
text_speech_client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE, name="en-US-Journey-F"
)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

def create_audio(text:str):
    
    print(f'Creating audio file for \'{text}\' | create_audio')# Log
    
    # Converts the text into ai synthesis text 
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Creates the voice response in binary audio form
    voice_response = text_speech_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    # File directory for storing audio 
    output_file = 'audio_data/output.wav'

    # Static file, removes and adds a new one everytime
    if os.path.exists(output_file): 
        os.remove(output_file)
    
    with wave.open(output_file, 'wb') as wav_file:
        # Sets the audio file parameter
        wav_file.setnchannels(1)  # Mono audio
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit audio)
        wav_file.setframerate(25000)  # Example sample rate (adjust if needed)
        
        # Write the raw audio content to the WAV file
        wav_file.writeframes(voice_response.audio_content)




