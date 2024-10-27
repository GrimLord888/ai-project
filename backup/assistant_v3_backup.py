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

# Start searching with Google Gemini
def ask_gemini(question):
    # modified_prompt = f"Give me a concise and brief answer to this question ({question}) in a maximum of 50 words"
    modified_prompt = f"Answer this question briefly: {question}"
    response = model.generate_content(modified_prompt)
    return response.text

# Play 45 seconds long music
def play_music():
    playsound('experience.mp3')

# Global flag to prevent "Are you okay?" from repeating after the first time of breathing exercise
initial_emotion_check_done = False

# Function to handle the breathing exercise routine
def breathing_exercise():
    speak_and_print("Let’s start by taking a slow breath in through your nose.")
    print('\n')
    time.sleep(15)
    speak_and_print("Now breathe out slowly through your mouth.")
    print('\n')
    time.sleep(20)
    speak_and_print("Great, let’s do it again. Breathe in slowly through your nose.")
    print('\n')
    time.sleep(15)
    speak_and_print("Now breathe out through your mouth. Nice and slow.")
    print('\n')
    time.sleep(20)
    speak_and_print("You’re doing well. One more time. Breathe in slowly.")
    print('\n')
    time.sleep(15)
    speak_and_print("And breathe out slowly.")
    print('\n')
    time.sleep(20)
    speak_and_print("Good job! You did it great!")
    print('\n')
    time.sleep(10)

    # Ask the user if they want to repeat the breathing exercise
    ask_repeat_exercise()

# Function to ask the user if they want to repeat the exercise
def ask_repeat_exercise():
    global initial_emotion_check_done  # Declare 'global' at the beginning of the function
    print("Hopefully you're feeling more relaxed. Would you like to repeat the exercises? (y/n)")
    speak("Hopefully you're feeling more relaxed. Would you like to repeat the exercises? yes or no")
    time.sleep(10)
    
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        print('Listening for repeat confirmation...')
        
        try:
            # Listen for a response with a timeout of 5 seconds
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            response = listener.recognize_google(voice).lower()
            print(f'User Response: {response}')
            
            if 'y' in response or 'yes' in response:
                print("Repeating the breathing exercise...")
                time.sleep(2)
                breathing_exercise()  # Repeat the exercise
            elif 'n' in response or 'no' in response:
                print("Proceeding to listen for the next command...")
                time.sleep(2)
                initial_emotion_check_done = True  # Set flag to prevent asking "Are you okay?" again
                run_assistant()  # Go back to listening for the next command
            else:
                print("Unrecognized response, asking again...")
                time.sleep(2)
                ask_repeat_exercise()  # Ask again recursively

        except sr.UnknownValueError:
            print("Sorry, I could not understand the response.")
            time.sleep(2)
            ask_repeat_exercise()

        except sr.WaitTimeoutError:
            print("No response received. Proceeding to listen for the next command...")
            time.sleep(2)
            initial_emotion_check_done = True  # Set flag to prevent asking "Are you okay?" again
            run_assistant()  # Proceed to normal listening mode

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
            time.sleep(2)
            speak_and_print("Keep going! I am rooting for you!")
            print('\n\n')
            time.sleep(5)
            return True

    # Check for negative emotions
    for word in negative_emotion_list:
        if word in command:
            speak_and_print("Are you okay?")
            time.sleep(2)
            # Wait for the user to respond
            with sr.Microphone() as source:
                print('Listening...')
                listener.adjust_for_ambient_noise(source)
                voice = listener.listen(source)
                response = listener.recognize_google(voice).lower()
                print(f'User Response: {response}')

                # Check if the response matches the no_list
                for no_word in no_list:
                    if no_word in response:
                        speak_and_print("It's okay. Everything will be fine. You are not alone. I am here for you.")
                        print('\n\n')
                        time.sleep(10)
                        return True

                # If the response matches the yes_list
                for yes_word in yes_list:
                    if yes_word in response:
                        time.sleep(2)
                        speak_and_print("That's great to hear!")
                        print('\n\n')
                        time.sleep(5)
                        return True

    return False  # Return False if no emotion was detected

# Function to handle emotion-based responses
def handle_another_emotion_(command):
    # Check for positive emotions
    for word in positive_emotion_list:
        if word in command:
            speak_and_print("Keep going! I am rooting for you!")
            print('\n\n')
            time.sleep(5)
            speak_and_print("However I realized your heart rate is high, let's us do some breathing exercises now.")
            print('\n')
            time.sleep(20)
            speak_and_print("Let’s start by taking a slow breath in through your nose.")
            print('\n')
            time.sleep(15)
            speak_and_print("Now breathe out slowly through your mouth.")
            print('\n')
            time.sleep(20)
            speak_and_print("Great, let’s do it again. Breathe in slowly through your nose.")
            print('\n')
            time.sleep(15)
            speak_and_print("Now breathe out through your mouth. Nice and slow.")
            print('\n')
            time.sleep(20)
            speak_and_print("You’re doing well. One more time. Breathe in slowly.")
            print('\n')
            time.sleep(15)
            speak_and_print("And breathe out slowly.")
            print('\n')
            time.sleep(20)
            speak_and_print("Good job! You did it great!")
            print('\n')
            time.sleep(10)
            speak_and_print("Now, please take a seat and have a rest. I will play some music for you")
            time.sleep(10)
            print("Playing music......")
            play_music()
            print('\n\n')
            time.sleep(1)

            return True
    
    # Check for yes list
    for word in yes_list:
        if word in command:
            speak_and_print("Keep going! I am rooting for you!")
            print('\n\n')
            time.sleep(5)
            speak_and_print("However I realized your heart rate is high, let's us do some breathing exercises now.")
            print('\n')
            time.sleep(20)
            speak_and_print("Let’s start by taking a slow breath in through your nose.")
            print('\n')
            time.sleep(15)
            speak_and_print("Now breathe out slowly through your mouth.")
            print('\n')
            time.sleep(20)
            speak_and_print("Great, let’s do it again. Breathe in slowly through your nose.")
            print('\n')
            time.sleep(15)
            speak_and_print("Now breathe out through your mouth. Nice and slow.")
            print('\n')
            time.sleep(20)
            speak_and_print("You’re doing well. One more time. Breathe in slowly.")
            print('\n')
            time.sleep(15)
            speak_and_print("And breathe out slowly.")
            print('\n')
            time.sleep(20)
            speak_and_print("Good job! You did it great!")
            print('\n')
            time.sleep(10)
            speak_and_print("Now, please take a seat and have a rest. I will play some music for you")
            time.sleep(10)
            print("Playing music......")
            play_music()
            print('\n\n')
            time.sleep(1)

            return True

    # Check for negative emotions
    for word in negative_emotion_list:
        if word in command:
            speak_and_print("It's okay. Everything will be fine. You are not alone. I am here for you.")
            print('\n\n')
            time.sleep(10)
            speak_and_print("To relieve your stress, let us start doing some breathing exercise now.")
            print('\n')
            time.sleep(20)
            speak_and_print("Let’s start by taking a slow breath in through your nose.")
            print('\n')
            time.sleep(15)
            speak_and_print("Now breathe out slowly through your mouth.")
            print('\n')
            time.sleep(20)
            speak_and_print("Great, let’s do it again. Breathe in slowly through your nose.")
            print('\n')
            time.sleep(15)
            speak_and_print("Now breathe out through your mouth. Nice and slow.")
            print('\n')
            time.sleep(20)
            speak_and_print("You’re doing well. One more time. Breathe in slowly.")
            print('\n')
            time.sleep(15)
            speak_and_print("And breathe out slowly.")
            print('\n')
            time.sleep(20)
            speak_and_print("Good job! You did it great!")
            print('\n')
            time.sleep(5)
            speak_and_print("Now, please take a seat and have a rest. I will play some music for you")
            time.sleep(10)
            print("Playing music......")
            play_music()
            print('\n\n')
            time.sleep(1)
            
            return True
    
    # Check for no list
    for word in no_list:
        if word in command:
            speak_and_print("It's okay. Everything will be fine. You are not alone. I am here for you.")
            print('\n\n')
            time.sleep(10)
            speak_and_print("To relieve your stress, let us start doing some breathing exercise now.")
            print('\n')
            time.sleep(20)
            speak_and_print("Let’s start by taking a slow breath in through your nose.")
            print('\n')
            time.sleep(15)
            speak_and_print("Now breathe out slowly through your mouth.")
            print('\n')
            time.sleep(20)
            speak_and_print("Great, let’s do it again. Breathe in slowly through your nose.")
            print('\n')
            time.sleep(15)
            speak_and_print("Now breathe out through your mouth. Nice and slow.")
            print('\n')
            time.sleep(20)
            speak_and_print("You’re doing well. One more time. Breathe in slowly.")
            print('\n')
            time.sleep(15)
            speak_and_print("And breathe out slowly.")
            print('\n')
            time.sleep(20)
            speak_and_print("Good job! You did it great!")
            print('\n')
            time.sleep(10)
            speak_and_print("Now, please take a seat and have a rest. I will play some music for you")
            time.sleep(10)
            print("Playing music......")
            play_music()
            print('\n\n')
            time.sleep(1)
            
            return True

    return False  # Return False if no emotion was detected

# Function of asking are you okay
# If the assistant does not understand the speech, it will call this function again until it gets a proper response or triggers the emergency timeout.
# The function returns True once a valid response is processed or after the emergency message is printed, which breaks the loop.
def ask_are_you_okay():
    global initial_emotion_check_done
    if initial_emotion_check_done:
        return  # Prevent re-asking once initial emotion check is done

    try:
        speak_and_print("Are you okay?")
        
        # Introduce a short delay to allow the assistant to finish speaking before listening
        time.sleep(2)

        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)

            try:
                # Listen for user input with a timeout of 5 seconds
                voice = listener.listen(source, timeout=5, phrase_time_limit=5)
                response = listener.recognize_google(voice).lower()
                print(f'User response: {response}')

                # Check if the response is too short or matches the assistant's own question
                if len(response.strip()) < 3 or "are you okay" in response:
                    print("Invalid response detected (possibly from the assistant's own voice). Asking again...")
                    return ask_are_you_okay()  # Recursively ask the question again
                
                handle_another_emotion_(response)
                return True  # If valid response, stop the loop

            except sr.WaitTimeoutError:
                # Trigger emergency action if no response is received within 5 seconds
                print("Emergency! No response received. Sending an emergency text message now......")
                speak_and_print("Emergency! No response received. Sending an emergency text message now......")
                time.sleep(10)
                return True  # Stop the loop after the emergency message

    except sr.UnknownValueError:
        # If the speech is detected but not understood or if no valid speech
        print("Sorry, I could not understand the audio. Asking again...")
        time.sleep(2)
        return ask_are_you_okay()  # Recursively ask the question again


# Main voice assistant loop
def run_assistant():
    global initial_emotion_check_done
    
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
            # Run the emotion handling first only once to ask "Are you okay?"
            # while not initial_emotion_check_done:
            #     ask_are_you_okay()  # Ask "Are you okay?" only once
            #     initial_emotion_check_done = True  # Set the flag to True after the first check
            try:
                speak('Listening...')
                time.sleep(2)
                # Listen for voice input
                with sr.Microphone() as source:
                    print('Listening...')
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
                    if len(command) < 3 or 'thank you for watching' in command or 'thanks for watching' in command or 'for watching' in command or 'subscribe' in command or 'listening' in command:
                        print("No speech detected. Detected transcription commonly mistaken for silence.")
                        print('\n\n')
                        continue  # Skip further processing if a silent-like transcription is detected

                    # Check if the command contains 'play' or 'playing'
                    # When doing the testing, it is suggested to say the following:
                    # (English song, Japanese song, and Chinese song were successfully tested)
                    # Please play the (language name) song: (title of the song + singer)
                    if 'play' in command or 'playing' in command:
                        song = command.replace('play', '').replace('playing', '')
                        speak_and_print(f'Playing {song.strip()} on YouTube...')
                        pywhatkit.playonyt(song.strip())
                        print('\n\n')
                        # Add a delay after the AI response
                        # time.sleep(180)
                        time.sleep(30)

                    # Ask it to tell us what is the current time
                    elif 'time' in command:
                        current_time = datetime.datetime.now().strftime('%I:%M %p')
                        speak_and_print('Current time is: ' + current_time)
                        print('\n\n')
                        time.sleep(5)

                    # Exit the voice assistant by just saying 'bye'
                    elif 'bye' in command or 'bye.' in command or 'bye!' in command or 'goodbye' in command or 'goodbye!' in command or 'goodbye.' in command:
                        speak_and_print("\nGoodbye! Enjoy the rest of your day!")
                        break
                    
                    # Check for emotions first
                    elif handle_emotion(command):
                        time.sleep(5)
                        continue  # Skip other commands if an emotion was detected and handled
                    
                    # Play music if the 'relax' keyword is in the sentence that the user said
                    elif 'music' in command or 'play music' in command or 'some music' in command:
                        print("Playing music......")
                        play_music()
                        print('\n\n')
                        time.sleep(1)

                    elif 'relax' in command or 'relaxing' in command or 'relaxed' in command or 'exercise' in command or 'exercise.' in command or 'exercises' in command or 'exercises.' in command or 'breathing' in command:
                        print("Starting breathing exercise routine.....")
                        breathing_exercise()
                        print('\n\n')
                        time.sleep(2)

                    # Otherwise, everything will be handle by gemini AI model for the response
                    else:
                        ai_response = ask_gemini(transcription)
                        speak_and_print(f'{ai_response}')
                        print('\n\n')
                        # Add a delay after the AI response
                        time.sleep(30)

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

    except KeyboardInterrupt:
        speak_and_print("\nGoodbye! Enjoy the rest of your day!")
        
    # Reset ALSA error handler to default after script finishes
    asound.snd_lib_error_set_handler(None)
    

run_assistant()