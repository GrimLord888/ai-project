import google.generativeai as genai
from gtts import gTTS
from playsound import playsound
import threading

# Google Gemini API setup
GOOGLE_API_KEY = 'AIzaSyA4P2D967E4JzIo977DX97PAfralZKSnQU'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Step 1
def ask_question(name):
    speak_and_print(f"Hey {name}. How are you feeling today? ")
    question = input(f"")
    return question

def ask_another_question(name):
    speak_and_print(f"Hey {name}. How can I help you? ")
    question = input(f"")
    return question

def classify_questions(question, name):
    goahead_with_web_search = False
    device_list = ['alarm', 'reminder', 'message', 'call']
    personal_list = ['who are you?', 'who are you', 'who created you?', 'who created you']
    girlboyfriend_list = ['girlfriend', 'Girlfriend', 'boyfriend', 'Boyfriend']
    emotion_list = ['stress', 'Stress', 'stressed', 'Stressed', 'pressure', 'Pressure', 'heart rate', 'Heart rate', 'heartrate', 'Heartrate', 'painful', 'Painful', 'sad', 'Sad',
                   'not good', 'Not good', 'angry', 'Angry', 'bad', 'Bad', 'cry', 'Cry', 'depressed', 'Depressed', 'suffered', 'Suffered', 'suffering', 'Suffering', 'suffer', 'Suffer',
                   'not happy', 'Not happy', 'yes', 'fine', 'good', 'happy', 'satisfied', 'satisfying', 'satify', 'excited', 'delighted', 'joyful', 'joy', 'hopeful', 'hope', 'lucky',
                   'fortune', 'fortunate', 'bright', 'encouraging', 'motivated', 'pleased', 'glad', 'thankful', 'grateful', 'not bad', 'cheerful', 'smiling']
    no_list = ['no', 'No', 'nope', 'Nope', 'not', 'Not', 'not okay', 'Not okay', 'no okay', 'No okay', 'not OK', 'Not OK', 'not Ok', 'Not Ok', 'not good', 'Not good', 'bad', 'Bad', 'cry', 'Cry', 'disaster', 'Disaster', 'suffered', 'Suffered', 'suffering', 'Suffering', 'suffer', 'Suffer', 'sad', 'Sad', 'not happy', 'Not happy']
    yes_list = ['yes', 'fine', 'good', 'happy', 'satisfied', 'satisfying', 'satify', 'excited', 'delighted', 'joyful', 'joy', 'hopeful', 'hope', 'lucky', 'fortune', 'fortunate', 'bright', 'encouraging', 'motivated', 'pleased', 'glad', 'thankful', 'grateful', 'not bad', 'cheerful', 'smiling']

    device = False
    for i in device_list:
        if i in question.lower():
            device = True

    if device:
        speak_and_print("This question is related to the device things, which is not supported in our Google Assistant!")
    
    personal_question = False
    for i in personal_list:
        if i in question.lower():
            personal_question = True

    if personal_question:
        speak_and_print("I am a personal assistant created by you!")

    girlboyfriend_question = False
    for i in girlboyfriend_list:
        if i in question.lower():
            girlboyfriend_question = True

    if girlboyfriend_question:
        speak_and_print("Yes, sure. Let us go marry then!")

    emotion_question = False
    for i in emotion_list:
        if i in question.lower():
            emotion_question = True

    if emotion_question:
        speak_and_print(f"Hey {name}, are you okay?")
        emotional_response = input(f"")
        for i in no_list:
            if i in emotional_response.lower():
                speak_and_print(f"Hey {name}! It's okay. Everything will be fine. You are not alone. I am here for you.")
                goahead_with_web_search = False
                break
        for i in yes_list:
            if i in emotional_response.lower():
                speak_and_print(f"Hey {name}! Keep going! I am rooting for you!")
                goahead_with_web_search = False
                break

    if device or personal_question or girlboyfriend_question or emotion_question:
        goahead_with_web_search = False
    else:
        goahead_with_web_search = True

    return goahead_with_web_search

def speak_and_print(text):
    # Start a new thread for speaking
    speak_thread = threading.Thread(target=speak, args=(text,))
    speak_thread.start()
    # Print the text at the same time
    print(text)

# Start searching with Google Gemini
def ask_gemini(question):
    modified_prompt = f"Give me a shortened answer to this question ({question}) in a maximum of 100 words"
    response = model.generate_content(modified_prompt)
    return response.text

def speak(answer):
    tts = gTTS(answer)
    tts.save('hello.mp3')
    playsound('hello.mp3')

# Start assembling everything together
have_any_other_questions = 'y'
name = ''

while have_any_other_questions == 'y':
    if name == '':
        speak_and_print('Hello! What is your name ?')
        name = input("")

    q = ask_question(name)

    go_ahead = classify_questions(q, name)
    if go_ahead:
        answer = ask_gemini(q)
        speak_and_print(answer)

    have_any_other_questions = input("Do you have any other questions ? (y/n)")

    while have_any_other_questions == 'y':
        if name != '':
            another_q = ask_another_question(name)
            go_ahead = classify_questions(another_q, name)
            if go_ahead:
                another_answer = ask_gemini(another_q)
                speak_and_print(another_answer)
        have_any_other_questions = input("Do you have any other questions ? (y/n)")

    if have_any_other_questions == 'n':
        speak_and_print("Bye! See you next time!")
