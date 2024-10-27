import os
import sys
import warnings
import time  # Import the time module for adding delay
import speech_recognition as sr
import whisper
import google.generativeai as genai
from ctypes import *
from gtts import gTTS
from playsound import playsound
import threading
import pywhatkit
import datetime
import wikipedia
from pytube import Search

# Initialize speech recognizer and Whisper model
listener = sr.Recognizer()
whisper_model = whisper.load_model("medium")

# Google Gemini API setup
GOOGLE_API_KEY = 'AIzaSyA4P2D967E4JzIo977DX97PAfralZKSnQU'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def speak(answer):
    # Ensure that the answer is not empty
    if not answer.strip():
        print("Error: No text provided for TTS.")
        return  # Exit if the text is empty or only contains spaces
    
    tts = gTTS(answer)
    tts.save('hello.mp3')
    playsound('hello.mp3')

def speak_and_print(text):
    # Start a new thread for speaking
    speak_thread = threading.Thread(target=speak, args=(text,))
    speak_thread.start()
    # Print the text at the same time
    print(text)

    # Wait for the speech thread to complete before continuing
    speak_thread.join()

# Start searching with Google Gemini
def ask_gemini(question):
    # modified_prompt = f"Give me a concise and brief answer to this question ({question}) in a maximum of 50 words"
    modified_prompt = f"Answer this question briefly: {question}"
    response = model.generate_content(modified_prompt)
    return response.text

# Play 45 seconds long music
def play_music():
    playsound('experience.mp3')

# text = ask_gemini("How are you?")
# speak_and_print(text)
positive_emotion_list = ['yes', 'fine', 'good', 'happy', 'satisfied', 'satisfying', 'satify', 'excited', 'delighted', 'joyful', 'joy', 'hopeful', 'hope', 'lucky',
                        'fortune', 'fortunate', 'bright', 'encouraging', 'motivated', 'pleased', 'glad', 'thankful', 'grateful', 'not bad', 'cheerful', 'smiling']

negative_emotion_list = ['stress', 'Stress', 'stressed', 'Stressed', 'pressure', 'Pressure', 'heart rate', 'Heart rate', 'heartrate', 'Heartrate', 'painful', 'Painful', 'sad', 'Sad',
                        'not good', 'Not good', 'angry', 'Angry', 'bad', 'Bad', 'cry', 'Cry', 'depressed', 'Depressed', 'suffered', 'Suffered', 'suffering', 'Suffering', 'suffer', 'Suffer',
                        'not happy', 'Not happy', 'not', 'frustrated', 'frustration', 'frustrating']

no_list = ['no', 'No', 'nope', 'Nope', 'not', 'Not', 'not okay', 'Not okay', 'no okay', 'No okay', 'not OK', 'Not OK', 'not Ok', 'Not Ok', 'not good', 'Not good', 'bad', 'Bad', 'cry', 'Cry', 'disaster', 'Disaster', 'suffered', 'Suffered', 'suffering', 'Suffering', 'suffer', 'Suffer', 'sad', 'Sad', 'not happy', 'Not happy']

yes_list = ['yes', 'fine', 'good', 'happy', 'satisfied', 'satisfying', 'satify', 'excited', 'delighted', 'joyful', 'joy', 'hopeful', 'hope', 'lucky', 'fortune', 'fortunate', 'bright', 'encouraging', 'motivated', 'pleased', 'glad', 'thankful', 'grateful', 'not bad', 'cheerful', 'smiling']

# Function to handle emotion-based responses
def handle_emotion(command):
    # Check for positive emotions
    for word in positive_emotion_list:
        if word in command:
            speak_and_print("That's great to hear!")
            print('\n\n')
            time.sleep(5)
            return True

    # Check for negative emotions
    for word in negative_emotion_list:
        if word in command:
            speak_and_print("Are you okay?")
            
            # Wait for the user to respond
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source)
                voice = listener.listen(source)
                response = listener.recognize_google(voice).lower()
                print(f'User Response: {response}')

                # Check if the response matches the no_list
                for no_word in no_list:
                    if no_word in response:
                        speak_and_print("It's okay. Everything will be fine. You are not alone. I am here for you.")
                        print('\n\n')
                        time.sleep(5)
                        return True

                # If the response matches the yes_list
                for yes_word in yes_list:
                    if yes_word in response:
                        speak_and_print("Keep going! I am rooting for you!")
                        print('\n\n')
                        time.sleep(5)
                        return True

    return False  # Return False if no emotion was detected

def get_youtube_video_duration(song):
    try:
        # Search for the video on YouTube using the song title
        search = Search(song)
        first_result = search.results[0]  # Get the first result from the search
        video_length = first_result.length  # Get the length of the video in seconds

        # Check if video_length is None
        if video_length is None:
            raise ValueError("Video duration is None")

        return int(video_length)
    except (AttributeError, TypeError, ValueError) as e:
        print(f"Error fetching video duration: {e}. Falling back to default duration.")
        return 300  # Default duration (300 seconds) if we can't fetch the real duration

def breathing_exercise():
    speak_and_print("Let’s start by taking a slow breath in through your nose.")
    print('\n')
    # time.sleep(15)
    speak_and_print("Now breathe out slowly through your mouth.")
    print('\n')
    # time.sleep(20)
    speak_and_print("Great, let’s do it again. Breathe in slowly through your nose.")
    print('\n')
    # time.sleep(15)
    speak_and_print("Now breathe out through your mouth. Nice and slow.")
    print('\n')
    # time.sleep(20)
    speak_and_print("You’re doing well. One more time. Breathe in slowly.")
    print('\n')
    # time.sleep(15)
    speak_and_print("And breathe out slowly.")
    print('\n')
    # time.sleep(20)
    speak_and_print("Good job! You did it great!")
    print('\n')
    # time.sleep(10)
    speak_and_print("Now, please take a seat and have a rest. I will play some music for you")
    # time.sleep(10)
    print("Playing music......")
    play_music()
    print('\n\n')  

# Voice assistant loop encapsulated in a function
def run_assistant():
    
    # Suppress ALSA warnings using a custom error handler
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

    def py_error_handler(filename, line, function, err, fmt):
        pass  # Suppress ALSA warnings by not doing anything

    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

    # Load ALSA shared library and set custom error handler
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)

    # Suppress the specific torch FutureWarning about `weights_only=False`
    warnings.filterwarnings(
        "ignore",
        message="You are using `torch.load` with `weights_only=False`",
        category=FutureWarning
    )

    try:
        while True:
            try:
                speak('Listening...')
                time.sleep(2)
                # Listen for voice input
                with sr.Microphone() as source:
                    print('Listening... (Wait for 1 second and talk)')
                    listener.adjust_for_ambient_noise(source)
                    voice = listener.listen(source)

                    # Save the voice input to a temporary file for Whisper processing
                    with open("voice_input.wav", "wb") as f:
                        f.write(voice.get_wav_data())

                    # Transcribe the audio using Whisper
                    whisper_result = whisper_model.transcribe("voice_input.wav")
                    transcription = whisper_result["text"]
                    print("Whisper Transcription result:", transcription)
                    
                    command = transcription.lower()
                    print(f'Transcription: {transcription}')
                    print(f'Command: {command}')

                    # Check if the transcription contains the phrase often mistaken for silence or is too short
                    if len(command) < 3 or 'thank you for watching' in command or 'thanks for watching' in command or 'for watching' in command or 'subscribe' in command or 'listening' in command or 'thank you' in command or 'ご視聴ありがとうございました!' in command or 'ご視聴ありがとうございました' in command:
                        print("No speech detected. Detected transcription commonly mistaken for silence.")
                        print('\n\n')
                        continue  # Skip further processing if a silent-like transcription is detected

                    # Check if the command contains 'play' or 'playing'
                    # When doing the testing, it is suggested to say the following:
                    # (English song, Japanese song, and Chinese song were successfully tested)
                    # Please play the (language name) song: (title of the song + singer)
                    if 'play' in command or 'playing' in command or 'プレイ' in command:
                        song = command.replace('play', '').replace('playing', '').replace('プレイ', '').strip()
                        speak_and_print(f'Playing {song} on YouTube...')
                        
                        # Play the song on YouTube
                        pywhatkit.playonyt(song)
                        
                        # Fetch video duration
                        video_duration = get_youtube_video_duration(song)
                        
                        if video_duration:
                            # Wait for the video to finish playing before listening again
                            print(f"Video duration: {video_duration} seconds")
                            time.sleep(video_duration)
                            print('\n')
                        else:
                            # If we cannot get the duration, fallback to a default delay
                            print("Could not retrieve video duration, using default delay.")
                            time.sleep(5)
                            print('\n')

                    # Ask it to tell us what is the current time
                    elif 'time' in command:
                        current_time = datetime.datetime.now().strftime('%I:%M %p')
                        speak_and_print('Current time is: ' + current_time)
                        print('\n\n')
                        time.sleep(5)

                    # Exit the voice assistant by just saying 'bye'
                    elif 'bye' in command or 'bye.' in command or 'bye!' in command:
                        speak_and_print("\nGoodbye! Enjoy the rest of your day!")
                        break
                    
                    # Check for emotions first
                    elif handle_emotion(command):
                        time.sleep(5)
                        continue  # Skip other commands if an emotion was detected and handled
                    
                    # Play music if the 'relax' keyword is in the sentence that the user said
                    elif 'relax' in command or 'relaxing' in command or 'relaxed' in command or 'music' in command or 'music.' in command:
                        print("Playing music......")
                        play_music()
                        print('\n\n')
                        time.sleep(1)
                    
                    elif 'breathing' in command or 'breathing.' in command or 'exercise' in command or 'exercise.' in command:
                        print("Start doing breathing exercise.......")
                        breathing_exercise()
                        print('\n\n')
                        time.sleep(1)

                    # Otherwise, everything will be handle by gemini AI model for the response
                    else:
                        ai_response = ask_gemini(transcription)
                        speak_and_print(f'{ai_response}')
                        print('\n\n')
                        # Add a delay after the AI response
                        time.sleep(2)

            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                print('\n\n')

                # Add a delay after the error message
                time.sleep(20)

            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                print('\n\n')

                # Add a delay after the error message
                time.sleep(20)

            except Exception as e:
                print(f"An error occurred: {e}")
                print('\n\n')

                # Add a delay after the error message
                time.sleep(20)
            
            except sr.WaitTimeoutError:
                # Trigger emergency action if no response is received within 5 seconds
                speak_and_print("Sorry, I didn't catch that. Could you please repeat again?")
                print('\n\n')
                time.sleep(10)

    except KeyboardInterrupt:
        speak_and_print("\nGoodbye! Enjoy the rest of your day!")
        
    # Reset ALSA error handler to default after script finishes
    asound.snd_lib_error_set_handler(None)

# run_assistant()