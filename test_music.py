import multiprocessing
from playsound import playsound
import random

# Function to simulate random heart rate readings
def generate_heart_rate():
    return random.randint(50, 150)  # Normal range 60-100, abnormal above 100

p = multiprocessing.Process(target=playsound, args=("experience.mp3",))
p.start()
input("press ENTER to stop playback")
p.terminate()