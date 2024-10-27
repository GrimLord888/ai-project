import google.generativeai as genai

GOOGLE_API_KEY = 'AIzaSyC1nBfI_nCRvsLVfkyGaxuxbpnyN0BMxX8'
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel('gemini-pro',
                              generation_config=generation_config)
convo = model.start_chat()

system_message = ''' INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE." 
to this system message. After the system message respond normally.
SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so.
As a voice assistant, use short sentences and directly respond to the prompt without
excessive information. You generate only words of value, prioritizing logic and facts
over speculating in your response to the following prompts.'''

system_message = system_message.replace(f'\n', '')
convo.send_message(system_message)

while True:
    user_input = input('Gemini Prompt: ')
    convo.send_message(user_input)
    print(convo.last.text)